# AI ChatBot Project

A modular and scalable AI chatbot solution with tiered functionality, from basic website integration to advanced multi-platform support.

## Project Structure

```
upwork_ai_chatbot/
├── src/
│   ├── chatbot_logic.py      # Core chatbot functionality
│   ├── data_loader.py        # Data ingestion and preparation
│   ├── web_embed_generator.py # Website integration
│   ├── api_integrations/     # API integration modules
│   └── platform_adapters/    # Platform-specific adapters
├── config/
│   ├── .env                  # Environment variables
│   └── chatbot_config.py     # Configuration settings
├── data/
│   ├── training_data.txt     # General training data
│   └── training_faqs.txt     # FAQ dataset
├── tests/
│   └── test_chatbot.py       # Test scripts
├── web/
│   └── index.html           # Test webpage
└── requirements.txt         # Python dependencies
```

## Features by Tier

### Tier 1: Basic Website Integration
- Simple chatbot with 9-step conversation flow
- Website embedding capability
- Basic FAQ handling
- Local testing support

### Tier 2: Multi-Platform & API Integration
- Extended conversation management
- Slack integration
- Basic external API calls
- Enhanced testing

### Tier 3: Advanced Business Integration
- Multiple platform support (WhatsApp, Telegram)
- Advanced conversational patterns
- Business API integration
- Monitoring and logging
- Comprehensive testing and deployment

## Setup Instructions

### Local Setup
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment:
   - Copy config/.env.template to config/.env
   - Add your OpenAI API key to .env

### Docker Setup
1. Make sure you have Docker and Docker Compose installed
2. Configure environment:
   - Copy config/.env.template to config/.env
   - Add your OpenAI API key to .env
3. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```
4. The chatbot will be available at http://localhost:5000

### Docker Commands
- Start the container: `docker-compose up`
- Stop the container: `docker-compose down`
- Rebuild the container: `docker-compose up --build`
- View logs: `docker-compose logs -f`

## Running the Chatbot

1. Start the web server:
   ```bash
   python src/web_embed_generator.py
   ```
2. Open web/index.html in a browser
3. Start chatting!

## Testing

Run the test script:
```bash
python tests/test_chatbot.py
```

## Adding Custom Functionality

### Adding New Platform Adapters
1. Create a new adapter in src/platform_adapters/
2. Implement the required interface
3. Update the main application to include the new adapter

### Adding API Integrations
1. Add new integration in src/api_integrations/
2. Update chatbot_logic.py to use the new integration
3. Update configuration as needed

## Documentation

For detailed documentation, see the comments in individual files and the docstrings in the code.

## License

MIT License - See LICENSE file for details
