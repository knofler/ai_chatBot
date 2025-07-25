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
            <title>AI Assistant - Your Intelligent Chat Partner</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        </head>
        <body class="bg-gray-50">
            <!-- Hero Section -->
            <div class="min-h-screen">
                <nav class="bg-white shadow-sm">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div class="flex justify-between h-16">
                            <div class="flex items-center">
                                <span class="text-2xl font-bold text-blue-600">AI Assistant</span>
                            </div>
                            <div class="flex items-center space-x-4">
                                <a href="#features" class="text-gray-600 hover:text-gray-900">Features</a>
                                <a href="#about" class="text-gray-600 hover:text-gray-900">About</a>
                                <button onclick="toggleChat()" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                                    Start Chat
                                </button>
                            </div>
                        </div>
                    </div>
                </nav>

                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                    <div class="lg:grid lg:grid-cols-12 lg:gap-8">
                        <div class="sm:text-center md:max-w-2xl md:mx-auto lg:col-span-6 lg:text-left">
                            <h1 class="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
                                Your Intelligent
                                <span class="text-blue-600">Chat Assistant</span>
                            </h1>
                            <p class="mt-3 text-base text-gray-500 sm:mt-5 sm:text-xl lg:text-lg xl:text-xl">
                                Experience the power of AI-driven conversations. Our intelligent chat assistant is here to help you with any questions, tasks, or discussions you might have.
                            </p>
                            <div class="mt-8 sm:max-w-lg sm:mx-auto sm:text-center lg:text-left">
                                <button onclick="toggleChat()" class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
                                    Start Chatting Now
                                    <i class="fas fa-arrow-right ml-2"></i>
                                </button>
                            </div>
                        </div>
                        <div class="mt-12 relative sm:max-w-lg sm:mx-auto lg:mt-0 lg:max-w-none lg:mx-0 lg:col-span-6 lg:flex lg:items-center">
                            <div class="relative mx-auto w-full rounded-lg shadow-lg lg:max-w-md">
                                <img class="w-full" src="https://images.unsplash.com/photo-1551434678-e076c223a692?ixlib=rb-1.2.1&auto=format&fit=crop&w=2850&q=80" alt="AI Chat">
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Chat Widget (Hidden by default) -->
            <div id="chat-widget" class="fixed bottom-4 right-4 w-96 bg-white rounded-lg shadow-xl transition-all duration-300 transform translate-y-full opacity-0">
                <div class="bg-blue-600 text-white px-4 py-3 rounded-t-lg flex justify-between items-center">
                    <h2 class="text-lg font-semibold">Chat with AI</h2>
                    <button onclick="toggleChat()" class="text-white hover:text-gray-200">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div id="chat-messages" class="h-96 p-4 overflow-y-auto space-y-4"></div>
                <div class="border-t p-4">
                    <div class="flex gap-2">
                        <input type="text" id="message-input" 
                            class="flex-1 rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                            placeholder="Type your message...">
                        <button onclick="sendMessage()" 
                            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Chat Toggle Button (Fixed) -->
            <button id="chat-toggle-btn" onclick="toggleChat()" 
                class="fixed bottom-4 right-4 w-14 h-14 bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-700 flex items-center justify-center">
                <i class="fas fa-comments text-xl"></i>
            </button>

            <script>
                function toggleChat() {
                    const chatWidget = document.getElementById('chat-widget');
                    const chatToggleBtn = document.getElementById('chat-toggle-btn');
                    
                    if (chatWidget.classList.contains('translate-y-full')) {
                        // Show chat
                        chatWidget.classList.remove('translate-y-full', 'opacity-0');
                        chatToggleBtn.classList.add('hidden');
                    } else {
                        // Hide chat
                        chatWidget.classList.add('translate-y-full', 'opacity-0');
                        chatToggleBtn.classList.remove('hidden');
                    }
                }

                function appendMessage(message, isUser) {
                    const div = document.createElement('div');
                    div.className = `p-3 rounded-lg ${isUser ? 'bg-blue-50 ml-auto text-blue-900' : 'bg-gray-50'} max-w-[80%] shadow-sm`;
                    
                    const textDiv = document.createElement('div');
                    textDiv.className = 'flex items-start gap-2';
                    
                    const icon = document.createElement('i');
                    icon.className = isUser ? 'fas fa-user text-blue-600 mt-1' : 'fas fa-robot text-gray-600 mt-1';
                    
                    const messageText = document.createElement('div');
                    messageText.textContent = message;
                    
                    textDiv.appendChild(icon);
                    textDiv.appendChild(messageText);
                    div.appendChild(textDiv);
                    
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
