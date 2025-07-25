"""
Web integration and JavaScript widget generator
"""
from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import sys
from pathlib import Path

# Add src directory to Python path
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

from chatbot_logic import Chatbot
from config import chatbot_config as config

# Set up template and static paths
template_dir = os.path.join(current_dir, 'templates')
static_dir = os.path.join(current_dir, 'static')

print(f"Template directory: {template_dir}")
print(f"Static directory: {static_dir}")

app = Flask(__name__, 
          static_folder=static_dir,
          template_folder=template_dir)

# Configure logging
if os.environ.get('FLASK_ENV') == 'development':
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.WARNING)  # Only show warnings and errors

print("Starting Flask application...")

# Global chatbot instance - lazy initialization
chatbot = None

def get_chatbot():
    """Get or create chatbot instance"""
    global chatbot
    if not chatbot:
        try:
            chatbot = Chatbot(lazy_load=True)
        except Exception as e:
            print(f"Warning: Chatbot initialization with error: {e}")
            chatbot = Chatbot(lazy_load=True, use_defaults=True)
    return chatbot

@app.route('/', methods=['GET'])
def index():
    """Serve the landing page"""
    try:
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI Chatbot</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-100 min-h-screen py-8">
            <div class="max-w-4xl mx-auto px-4">
                <div class="bg-white rounded-lg shadow-lg overflow-hidden">
                    <div class="p-6">
                        <h1 class="text-3xl font-bold text-gray-800 mb-4">AI Chatbot</h1>
                        <div class="border rounded-lg">
                            <div class="bg-blue-600 text-white px-4 py-3">
                                <h2 class="text-lg font-semibold">Chat with AI</h2>
                            </div>
                            <div id="chat-messages" class="h-[400px] p-4 overflow-y-auto space-y-4"></div>
                            <div class="border-t p-4 flex gap-4">
                                <input type="text" id="message-input" 
                                    class="flex-1 rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                    placeholder="Type your message...">
                                <button onclick="sendMessage()" 
                                    class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
                                    Send
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                function appendMessage(message, isUser) {
                    const div = document.createElement('div');
                    div.className = `p-4 rounded-lg ${isUser ? 'bg-blue-50 ml-auto' : 'bg-gray-50'} max-w-[80%]`;
                    div.textContent = message;
                    document.getElementById('chat-messages').appendChild(div);
                    div.scrollIntoView({ behavior: 'smooth' });
                }

                function sendMessage() {
                    const input = document.getElementById('message-input');
                    const message = input.value.trim();
                    if (!message) return;
                    
                    appendMessage(message, true);
                    input.value = '';

                    fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            appendMessage('Error: ' + data.error, false);
                        } else {
                            appendMessage(data.response, false);
                        }
                    })
                    .catch(() => {
                        appendMessage('Could not connect to AI Agent. Please try again later.', false);
                    });
                }

                document.getElementById('message-input').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        sendMessage();
                    }
                });
            </script>
        </body>
        </html>
        """
        return html
    except Exception as e:
        print(f"Error rendering template: {str(e)}")
        # Return a basic HTML page for debugging
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI Chatbot</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-100 p-8">
            <div class="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow-lg">
                <h1 class="text-3xl font-bold mb-4">AI Chatbot</h1>
                <p class="text-gray-600">Template error: {str(e)}</p>
                <p class="mt-4">Debug info:</p>
                <pre class="bg-gray-100 p-4 rounded mt-2">
Template path: {app.template_folder}
Static path: {app.static_folder}
                </pre>
            </div>
        </body>
        </html>
        """

@app.route('/test')
def test_page():
    """Test template rendering"""
    try:
        return render_template('test.html')
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Docker"""
    return jsonify({"status": "healthy"}), 200

@app.route('/.well-known/appspecific/com.chrome.devtools.json')
def handle_chrome_devtools():
    """Handle Chrome DevTools requests to prevent 404 logs"""
    return jsonify({}), 200

@app.route('/reload-data', methods=['POST'])
def reload_data():
    """Endpoint to reload training data without restarting server"""
    try:
        bot = get_chatbot()
        bot.reload_training_data()
        return jsonify({"status": "success", "message": "Training data reloaded"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/chat', methods=['POST'])
async def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        bot = get_chatbot()
        response = await bot.get_response(user_message)
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_widget_code(server_url):
    """Generate the JavaScript code for the chat widget"""
    return f"""
<!-- ChatBot Widget -->
<div id="chatbot-widget" style="position: fixed; bottom: 20px; right: 20px; width: 300px; height: 400px; background: white; border: 1px solid #ccc; border-radius: 8px; overflow: hidden; display: flex; flex-direction: column;">
    <div style="padding: 10px; background: #007bff; color: white;">Chat with AI</div>
    <div id="chat-messages" style="flex: 1; overflow-y: auto; padding: 10px;"></div>
    <div style="padding: 10px; border-top: 1px solid #ccc;">
        <input type="text" id="user-input" placeholder="Type your message..." style="width: 80%; padding: 5px;">
        <button onclick="sendMessage()" style="width: 18%; padding: 5px;">Send</button>
    </div>
</div>

<script>
const serverUrl = '{server_url}';

function appendMessage(message, isUser) {{
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.style.margin = '5px';
    messageDiv.style.padding = '5px';
    messageDiv.style.borderRadius = '5px';
    messageDiv.style.backgroundColor = isUser ? '#e9ecef' : '#f8f9fa';
    messageDiv.textContent = message;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}}

async function sendMessage() {{
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    appendMessage(message, true);
    input.value = '';

    try {{
        const response = await fetch(`${{serverUrl}}/chat`, {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{ message }})
        }});

        const data = await response.json();
        if (data.error) {{
            appendMessage('Error: ' + data.error, false);
        }} else {{
            appendMessage(data.response, false);
        }}
    }} catch (error) {{
        appendMessage('Error: Could not connect to server', false);
    }}
}}

document.getElementById('user-input').addEventListener('keypress', function(e) {{
    if (e.key === 'Enter') {{
        sendMessage();
    }}
}});
</script>
"""

def run_server():
    """Run the Flask server"""
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    )
