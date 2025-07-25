"""
Data loader for training data and FAQs
"""
import os

class DataLoader:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.faqs = {}
        self.training_data = ""

    def load_faqs(self, filename="training_faqs.txt"):
        """Load FAQs from a text file"""
        try:
            with open(os.path.join(self.data_dir, filename), 'r') as f:
                content = f.read().strip().split('\n\n')
                for qa in content:
                    if '?' in qa:
                        q, a = qa.split('?', 1)
                        self.faqs[q.strip() + '?'] = a.strip()
            return True
        except FileNotFoundError:
            print(f"Warning: {filename} not found in {self.data_dir}")
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

    def get_context(self):
        """Get combined context for the chatbot"""
        context = ""
        if self.training_data:
            context += self.training_data + "\n\n"
        if self.faqs:
            context += "Frequently Asked Questions:\n"
            for q, a in self.faqs.items():
                context += f"Q: {q}\nA: {a}\n\n"
        return context.strip()
