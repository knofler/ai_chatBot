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
            <title>AI Assistant - Next Generation Conversational AI</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <script>
                tailwind.config = {
                    theme: {
                        extend: {
                            colors: {
                                primary: {
                                    50: '#f0f9ff',
                                    100: '#e0f2fe',
                                    500: '#0ea5e9',
                                    600: '#0284c7',
                                    700: '#0369a1',
                                }
                            }
                        }
                    }
                }
            </script>
            <style>
                .gradient-text {
                    background: linear-gradient(45deg, #0ea5e9, #6366f1);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }
                .gradient-bg {
                    background: linear-gradient(135deg, #0ea5e9, #6366f1);
                }
            </style>
        </head>
        <body class="bg-gray-50">
            <!-- Sticky Navigation -->
            <nav class="fixed w-full z-50 bg-white/80 backdrop-blur-md shadow-sm">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="flex justify-between h-16">
                        <div class="flex items-center">
                            <span class="text-2xl font-bold gradient-text">AI Assistant</span>
                        </div>
                        <div class="hidden md:flex items-center space-x-8">
                            <a href="#features" class="text-gray-600 hover:text-gray-900">Features</a>
                            <a href="#how-it-works" class="text-gray-600 hover:text-gray-900">How It Works</a>
                            <a href="#pricing" class="text-gray-600 hover:text-gray-900">Pricing</a>
                            <a href="#testimonials" class="text-gray-600 hover:text-gray-900">Testimonials</a>
                            <button onclick="toggleChat()" class="gradient-bg text-white px-4 py-2 rounded-lg hover:opacity-90 transition-all">
                                Start Chat
                            </button>
                        </div>
                        <button class="md:hidden gradient-bg text-white px-4 rounded-lg">
                            <i class="fas fa-bars"></i>
                        </button>
                    </div>
                </div>
            </nav>

            <!-- Hero Section -->
            <div class="pt-24 pb-16 md:pt-32 md:pb-24">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="lg:grid lg:grid-cols-12 lg:gap-8">
                        <div class="sm:text-center md:max-w-2xl md:mx-auto lg:col-span-6 lg:text-left lg:flex lg:flex-col lg:justify-center">
                            <div class="mb-8">
                                <span class="inline-block gradient-bg text-white text-sm font-semibold px-4 py-1 rounded-full">
                                    AI-Powered Communication
                                </span>
                            </div>
                            <h1 class="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl lg:text-5xl xl:text-6xl">
                                Next Generation
                                <span class="gradient-text block">Conversational AI</span>
                            </h1>
                            <p class="mt-6 text-base text-gray-500 sm:mt-8 sm:text-xl lg:text-lg xl:text-xl">
                                Transform your business communication with our advanced AI assistant. Get instant responses, 24/7 support, and human-like conversations powered by cutting-edge machine learning.
                            </p>
                            <div class="mt-8 sm:mt-12 flex flex-col sm:flex-row gap-4 sm:items-center lg:justify-start">
                                <button onclick="toggleChat()" class="gradient-bg text-white px-8 py-4 rounded-xl hover:opacity-90 transition-all text-lg font-medium flex items-center justify-center">
                                    Try AI Chat Now
                                    <i class="fas fa-arrow-right ml-2"></i>
                                </button>
                                <a href="#how-it-works" class="text-gray-600 hover:text-gray-900 flex items-center justify-center">
                                    <i class="fas fa-play-circle text-primary-500 mr-2"></i>
                                    See how it works
                                </a>
                            </div>
                        </div>
                        <div class="mt-12 relative sm:max-w-lg sm:mx-auto lg:mt-0 lg:max-w-none lg:mx-0 lg:col-span-6 lg:flex lg:items-center">
                            <div class="relative mx-auto w-full rounded-2xl shadow-xl lg:max-w-md overflow-hidden">
                                <img class="w-full" src="https://images.unsplash.com/photo-1583508915901-b5f84c1dcde1?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80" alt="AI Chat Interface">
                                <!-- Floating Features -->
                                <div class="absolute -right-4 top-1/4 bg-white rounded-lg shadow-lg p-4 flex items-center space-x-3">
                                    <div class="w-8 h-8 gradient-bg rounded-full flex items-center justify-center">
                                        <i class="fas fa-robot text-white"></i>
                                    </div>
                                    <div>
                                        <div class="text-sm font-semibold">AI Powered</div>
                                        <div class="text-xs text-gray-500">24/7 Available</div>
                                    </div>
                                </div>
                                <div class="absolute -left-4 top-2/3 bg-white rounded-lg shadow-lg p-4 flex items-center space-x-3">
                                    <div class="w-8 h-8 gradient-bg rounded-full flex items-center justify-center">
                                        <i class="fas fa-bolt text-white"></i>
                                    </div>
                                    <div>
                                        <div class="text-sm font-semibold">Fast Responses</div>
                                        <div class="text-xs text-gray-500">Under 1 second</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Stats Section -->
            <div class="gradient-bg">
                <div class="max-w-7xl mx-auto py-12 px-4 sm:py-16 sm:px-6 lg:px-8">
                    <div class="grid grid-cols-2 gap-4 md:grid-cols-4">
                        <div class="text-center">
                            <div class="text-4xl font-bold text-white">99%</div>
                            <div class="text-primary-100 mt-1">Response Rate</div>
                        </div>
                        <div class="text-center">
                            <div class="text-4xl font-bold text-white">24/7</div>
                            <div class="text-primary-100 mt-1">Availability</div>
                        </div>
                        <div class="text-center">
                            <div class="text-4xl font-bold text-white">1s</div>
                            <div class="text-primary-100 mt-1">Response Time</div>
                        </div>
                        <div class="text-center">
                            <div class="text-4xl font-bold text-white">10k+</div>
                            <div class="text-primary-100 mt-1">Happy Users</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Features Section -->
            <div id="features" class="py-16 bg-white">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="text-center">
                        <h2 class="text-3xl font-bold gradient-text mb-2">Powerful Features</h2>
                        <p class="text-gray-500 text-xl">Everything you need for perfect communication</p>
                    </div>
                    <div class="mt-12 grid gap-8 md:grid-cols-2 lg:grid-cols-3">
                        <div class="p-6 rounded-xl border border-gray-200 hover:shadow-lg transition-all">
                            <div class="w-12 h-12 gradient-bg rounded-lg flex items-center justify-center mb-4">
                                <i class="fas fa-brain text-white text-xl"></i>
                            </div>
                            <h3 class="text-xl font-semibold mb-2">Advanced AI</h3>
                            <p class="text-gray-600">State-of-the-art language models for human-like conversations.</p>
                        </div>
                        <div class="p-6 rounded-xl border border-gray-200 hover:shadow-lg transition-all">
                            <div class="w-12 h-12 gradient-bg rounded-lg flex items-center justify-center mb-4">
                                <i class="fas fa-bolt text-white text-xl"></i>
                            </div>
                            <h3 class="text-xl font-semibold mb-2">Real-time Responses</h3>
                            <p class="text-gray-600">Get instant answers to your questions, available 24/7.</p>
                        </div>
                        <div class="p-6 rounded-xl border border-gray-200 hover:shadow-lg transition-all">
                            <div class="w-12 h-12 gradient-bg rounded-lg flex items-center justify-center mb-4">
                                <i class="fas fa-lock text-white text-xl"></i>
                            </div>
                            <h3 class="text-xl font-semibold mb-2">Secure & Private</h3>
                            <p class="text-gray-600">Enterprise-grade security for your sensitive conversations.</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Testimonials Section -->
            <div id="testimonials" class="py-16 bg-gray-50">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="text-center mb-12">
                        <h2 class="text-3xl font-bold gradient-text mb-2">What Our Users Say</h2>
                        <p class="text-gray-500 text-xl">Trusted by thousands of companies worldwide</p>
                    </div>
                    <div class="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
                        <div class="bg-white p-6 rounded-xl shadow-md">
                            <div class="flex items-center mb-4">
                                <img class="w-12 h-12 rounded-full" src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" alt="User">
                                <div class="ml-4">
                                    <div class="font-semibold">John Doe</div>
                                    <div class="text-gray-500 text-sm">CEO, TechCorp</div>
                                </div>
                            </div>
                            <p class="text-gray-600">"This AI assistant has transformed how we handle customer support. Response times are down 90% and customer satisfaction is up!"</p>
                            <div class="mt-4 flex text-primary-500">
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                            </div>
                        </div>
                        <div class="bg-white p-6 rounded-xl shadow-md">
                            <div class="flex items-center mb-4">
                                <img class="w-12 h-12 rounded-full" src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" alt="User">
                                <div class="ml-4">
                                    <div class="font-semibold">Sarah Smith</div>
                                    <div class="text-gray-500 text-sm">Product Manager</div>
                                </div>
                            </div>
                            <p class="text-gray-600">"The natural language understanding is impressive. It feels like chatting with a human expert who knows everything about our products."</p>
                            <div class="mt-4 flex text-primary-500">
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                            </div>
                        </div>
                        <div class="bg-white p-6 rounded-xl shadow-md">
                            <div class="flex items-center mb-4">
                                <img class="w-12 h-12 rounded-full" src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" alt="User">
                                <div class="ml-4">
                                    <div class="font-semibold">Mike Johnson</div>
                                    <div class="text-gray-500 text-sm">Support Lead</div>
                                </div>
                            </div>
                            <p class="text-gray-600">"We've seen a 70% reduction in support tickets since implementing this AI assistant. The ROI has been incredible."</p>
                            <div class="mt-4 flex text-primary-500">
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star-half-alt"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Pricing Section -->
            <div id="pricing" class="py-16 bg-white">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="text-center mb-12">
                        <h2 class="text-3xl font-bold gradient-text mb-2">Simple, Transparent Pricing</h2>
                        <p class="text-gray-500 text-xl">Choose the plan that works best for you</p>
                    </div>
                    <div class="grid gap-8 md:grid-cols-3">
                        <div class="border border-gray-200 rounded-xl p-8 hover:shadow-lg transition-all">
                            <div class="text-center mb-6">
                                <h3 class="text-xl font-semibold mb-2">Starter</h3>
                                <div class="text-4xl font-bold mb-2">$29<span class="text-gray-500 text-base font-normal">/mo</span></div>
                                <p class="text-gray-500">Perfect for small businesses</p>
                            </div>
                            <ul class="space-y-4 mb-8">
                                <li class="flex items-center">
                                    <i class="fas fa-check text-green-500 mr-2"></i>
                                    <span>1,000 messages/month</span>
                                </li>
                                <li class="flex items-center">
                                    <i class="fas fa-check text-green-500 mr-2"></i>
                                    <span>Basic AI features</span>
                                </li>
                                <li class="flex items-center">
                                    <i class="fas fa-check text-green-500 mr-2"></i>
                                    <span>Email support</span>
                                </li>
                            </ul>
                            <button onclick="toggleChat()" class="w-full py-2 px-4 border border-primary-500 text-primary-500 rounded-lg hover:bg-primary-50 transition-colors">
                                Start Free Trial
                            </button>
                        </div>
                        <div class="border-2 border-primary-500 rounded-xl p-8 shadow-lg relative">
                            <div class="absolute top-0 right-4 transform -translate-y-1/2 bg-primary-500 text-white px-4 py-1 rounded-full text-sm">
                                Popular
                            </div>
                            <div class="text-center mb-6">
                                <h3 class="text-xl font-semibold mb-2">Professional</h3>
                                <div class="text-4xl font-bold mb-2">$99<span class="text-gray-500 text-base font-normal">/mo</span></div>
                                <p class="text-gray-500">For growing teams</p>
                            </div>
                            <ul class="space-y-4 mb-8">
                                <li class="flex items-center">
                                    <i class="fas fa-check text-green-500 mr-2"></i>
                                    <span>10,000 messages/month</span>
                                </li>
                                <li class="flex items-center">
                                    <i class="fas fa-check text-green-500 mr-2"></i>
                                    <span>Advanced AI features</span>
                                </li>
                                <li class="flex items-center">
                                    <i class="fas fa-check text-green-500 mr-2"></i>
                                    <span>Priority support</span>
                                </li>
                                <li class="flex items-center">
                                    <i class="fas fa-check text-green-500 mr-2"></i>
                                    <span>Custom integrations</span>
                                </li>
                            </ul>
                            <button onclick="toggleChat()" class="w-full py-2 px-4 gradient-bg text-white rounded-lg hover:opacity-90 transition-opacity">
                                Start Free Trial
                            </button>
                        </div>
                        <div class="border border-gray-200 rounded-xl p-8 hover:shadow-lg transition-all">
                            <div class="text-center mb-6">
                                <h3 class="text-xl font-semibold mb-2">Enterprise</h3>
                                <div class="text-4xl font-bold mb-2">Custom</div>
                                <p class="text-gray-500">For large organizations</p>
                            </div>
                            <ul class="space-y-4 mb-8">
                                <li class="flex items-center">
                                    <i class="fas fa-check text-green-500 mr-2"></i>
                                    <span>Unlimited messages</span>
                                </li>
                                <li class="flex items-center">
                                    <i class="fas fa-check text-green-500 mr-2"></i>
                                    <span>Custom AI training</span>
                                </li>
                                <li class="flex items-center">
                                    <i class="fas fa-check text-green-500 mr-2"></i>
                                    <span>24/7 phone support</span>
                                </li>
                                <li class="flex items-center">
                                    <i class="fas fa-check text-green-500 mr-2"></i>
                                    <span>SLA guarantee</span>
                                </li>
                            </ul>
                            <button onclick="toggleChat()" class="w-full py-2 px-4 border border-primary-500 text-primary-500 rounded-lg hover:bg-primary-50 transition-colors">
                                Contact Sales
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Footer -->
            <footer class="bg-gray-900 text-white py-12">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
                        <div>
                            <h3 class="text-lg font-semibold mb-4">Product</h3>
                            <ul class="space-y-2">
                                <li><a href="#features" class="text-gray-400 hover:text-white">Features</a></li>
                                <li><a href="#pricing" class="text-gray-400 hover:text-white">Pricing</a></li>
                                <li><a href="#testimonials" class="text-gray-400 hover:text-white">Testimonials</a></li>
                            </ul>
                        </div>
                        <div>
                            <h3 class="text-lg font-semibold mb-4">Company</h3>
                            <ul class="space-y-2">
                                <li><a href="#about" class="text-gray-400 hover:text-white">About</a></li>
                                <li><a href="#careers" class="text-gray-400 hover:text-white">Careers</a></li>
                                <li><a href="#contact" class="text-gray-400 hover:text-white">Contact</a></li>
                            </ul>
                        </div>
                        <div>
                            <h3 class="text-lg font-semibold mb-4">Resources</h3>
                            <ul class="space-y-2">
                                <li><a href="#docs" class="text-gray-400 hover:text-white">Documentation</a></li>
                                <li><a href="#api" class="text-gray-400 hover:text-white">API</a></li>
                                <li><a href="#blog" class="text-gray-400 hover:text-white">Blog</a></li>
                            </ul>
                        </div>
                        <div>
                            <h3 class="text-lg font-semibold mb-4">Legal</h3>
                            <ul class="space-y-2">
                                <li><a href="#privacy" class="text-gray-400 hover:text-white">Privacy Policy</a></li>
                                <li><a href="#terms" class="text-gray-400 hover:text-white">Terms of Service</a></li>
                                <li><a href="#cookies" class="text-gray-400 hover:text-white">Cookie Policy</a></li>
                            </ul>
                        </div>
                    </div>
                    <div class="mt-8 pt-8 border-t border-gray-800 text-center text-gray-400">
                        <p>&copy; 2025 AI Assistant. All rights reserved.</p>
                    </div>
                </div>
            </footer>

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
