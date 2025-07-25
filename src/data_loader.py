"""
Data loader for training data and FAQs
"""
import os

class DataLoader:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.faqs = {
            "What is this chatbot?": "I am an AI assistant ready to help you with your questions.",
            "How can I help you?": "I can assist you with various tasks and answer your questions.",
        }
        self.training_data = "I am a helpful AI assistant designed to provide clear and concise responses."
        
        # Create data directory if it doesn't exist
        try:
            os.makedirs(self.data_dir, exist_ok=True)
        except Exception as e:
            print(f"Note: Using default configuration: {e}")
            return

        # Try to load data, but use defaults if unavailable
        try:
            if self.load_training_data():
                print("Successfully loaded training data")
        except Exception as e:
            print(f"Note: Using default training data: {e}")
            
        try:
            if self.load_faqs():
                print("Successfully loaded FAQs")
        except Exception as e:
            print(f"Note: Using default FAQs: {e}")

    def load_faqs(self, filename="training_faqs.txt"):
        """Load FAQs from a text file"""
        try:
            with open(os.path.join(self.data_dir, filename), 'r') as f:
                content = f.read().strip().split('\n\n')
                loaded_faqs = {}
                for qa in content:
                    if '?' in qa:
                        q, a = qa.split('?', 1)
                        loaded_faqs[q.strip() + '?'] = a.strip()
                if loaded_faqs:  # Only update if we loaded something
                    self.faqs.update(loaded_faqs)
                return True
        except FileNotFoundError:
            # Just use default FAQs
            return False

    def load_training_data(self, filename="training_data.txt"):
        """Load general training data"""
        try:
            with open(os.path.join(self.data_dir, filename), 'r') as f:
                self.training_data = f.read().strip()
            return True
        except FileNotFoundError:
            print(f"Warning: {filename} not found in {self.data_dir}")
            return False

    def _init_default_data(self):
        """Initialize with default data if no files exist"""
        default_faqs = {
            "What is this chatbot?": "This is an AI-powered assistant designed to help answer questions and provide information.",
            "How can I help you?": "I can answer questions, provide information, and assist with various tasks.",
            "What can you do?": "I can understand and respond to your questions, help with basic tasks, and provide relevant information."
        }
        
        default_training = "I am a helpful AI assistant. I aim to be friendly, informative, and concise."
        
        # Save default data if files don't exist
        if not os.path.exists(os.path.join(self.data_dir, "training_faqs.txt")):
            faq_content = ""
            for q, a in default_faqs.items():
                faq_content += f"{q}\n{a}\n\n"
            try:
                with open(os.path.join(self.data_dir, "training_faqs.txt"), 'w') as f:
                    f.write(faq_content.strip())
                self.faqs = default_faqs
            except Exception as e:
                print(f"Warning: Could not write default FAQs: {str(e)}")
                self.faqs = default_faqs

        if not os.path.exists(os.path.join(self.data_dir, "training_data.txt")):
            try:
                with open(os.path.join(self.data_dir, "training_data.txt"), 'w') as f:
                    f.write(default_training)
                self.training_data = default_training
            except Exception as e:
                print(f"Warning: Could not write default training data: {str(e)}")
                self.training_data = default_training

    def get_context(self):
        """Get combined context for the chatbot"""
        context = "I am a helpful AI assistant ready to help you.\n\n"
        
        # Add training data if available
        if self.training_data:
            context += f"Additional Training Context:\n{self.training_data}\n\n"
            
        # Add FAQs if available
        if self.faqs:
            context += "Frequently Asked Questions:\n"
            for q, a in self.faqs.items():
                context += f"Q: {q}\nA: {a}\n\n"
                
        return context.strip()
