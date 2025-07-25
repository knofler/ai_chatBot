"""
Test script for the chatbot
"""
import asyncio
from src.chatbot_logic import Chatbot

async def test_conversation():
    chatbot = Chatbot()
    
    test_inputs = [
        "Hello, how can you help me?",
        "What services do you provide?",
        "Can you tell me more about your pricing?",
    ]
    
    print("Starting test conversation...")
    print("-" * 50)
    
    for user_input in test_inputs:
        print(f"\nUser: {user_input}")
        response = await chatbot.get_response(user_input)
        print(f"Bot: {response}")
        
    print("\nTest conversation completed.")

if __name__ == "__main__":
    asyncio.run(test_conversation())
