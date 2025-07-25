"""
Core chatbot logic for handling conversations
"""
import os
import openai
from dotenv import load_dotenv
from config import chatbot_config as config
from src.data_loader import DataLoader

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../config/.env'))
openai.api_key = os.getenv('OPENAI_API_KEY')

class Chatbot:
    def __init__(self, lazy_load=False, use_defaults=False):
        self.conversation_steps = 0
        self.conversation_history = []
        self.data_loader = None
        self._data_initialized = False
        if not lazy_load:
            self.initialize_data_loader(use_defaults)

    def _create_prompt(self, user_input):
        """Create the prompt for the OpenAI API"""
        # Ensure data is loaded before creating prompt
        if not self._data_initialized:
            self.initialize_data_loader()
        
        context = self.data_loader.get_context() if self.data_loader else ""
        
        # Build conversation history
        conv_history = ""
        for msg in self.conversation_history[-5:]:  # Last 5 messages for context
            conv_history += f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}\n"

        # Combine all parts
        prompt = f"{config.DEFAULT_SYSTEM_PROMPT}\n\nContext:\n{context}\n\nConversation History:\n{conv_history}\nUser: {user_input}\nAssistant:"
        return prompt

    def initialize_data_loader(self, use_defaults=False):
        """Initialize or reinitialize the data loader"""
        try:
            data_path = os.path.join(os.path.dirname(__file__), '../data')
            self.data_loader = DataLoader(data_path, use_defaults=use_defaults)
            self._data_initialized = True
        except Exception as e:
            print(f"Warning: Data loader initialization failed: {e}")
            if use_defaults:
                self.data_loader = DataLoader(data_path, use_defaults=True)
                self._data_initialized = True
            else:
                raise

    def reload_training_data(self):
        """Reload training data and FAQs"""
        try:
            if not self.data_loader:
                self.initialize_data_loader()
            self.data_loader.load_training_data()
            self.data_loader.load_faqs()
            return True
        except Exception as e:
            print(f"Warning: Failed to reload training data: {e}")
            return False

    async def get_response(self, user_input):
        """Get a response from the chatbot"""
        if self.conversation_steps >= config.MAX_CONVERSATION_STEPS:
            return "I apologize, but we've reached the maximum number of conversation steps. Please start a new conversation."

        try:
            # Add user input to history
            self.conversation_history.append({"role": "user", "content": user_input})

            # Create completion with OpenAI
            response = openai.ChatCompletion.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": config.DEFAULT_SYSTEM_PROMPT},
                    {"role": "user", "content": self._create_prompt(user_input)}
                ],
                max_tokens=config.MAX_TOKENS,
                temperature=config.TEMPERATURE
            )

            # Extract and store response
            bot_response = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": bot_response})
            self.conversation_steps += 1

            return bot_response

        except Exception as e:
            print(f"Error getting response: {str(e)}")
            return "I apologize, but I encountered an error. Please try again."

    def reset_conversation(self):
        """Reset the conversation"""
        self.conversation_steps = 0
        self.conversation_history = []
