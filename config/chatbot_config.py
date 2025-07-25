"""
Configuration settings for the chatbot
"""

# Conversation flow settings
MAX_CONVERSATION_STEPS = 9
DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant. Be concise and clear in your responses.
Follow the conversation flow naturally and provide relevant information."""

# OpenAI settings
OPENAI_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 150
TEMPERATURE = 0.7

# Web integration settings
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = False
