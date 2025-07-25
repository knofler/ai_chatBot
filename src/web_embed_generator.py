"""
Web integration and JavaScript widget generator
"""
from flask import Flask, request, jsonify
from src.chatbot_logic import Chatbot
from config import chatbot_config as config

app = Flask(__name__)
chatbot = Chatbot()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Docker"""
    return jsonify({"status": "healthy"}), 200

@app.route('/chat', methods=['POST'])
async def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        response = await chatbot.get_response(user_message)
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
