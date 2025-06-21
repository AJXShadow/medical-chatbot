# Generative AI Medical Chatbot

## Overview
Generative AI Medical Chatbot is an AI-powered virtual assistant designed to provide reliable medical information, preliminary symptom assessment, and healthcare guidance. It leverages large language models and vector search to answer user queries based on a medical encyclopedia PDF.

## Features
- **Symptom Assessment:** Users can describe symptoms and receive possible causes and recommendations.
- **Medical Q&A:** Provides information on conditions, medications, and treatments using LLMs and PDF data.
- **Healthcare Navigation:** Can be extended to help users find healthcare facilities and specialists.
- **Privacy-Focused:** User health data is not stored.
- **Concise, Contextual Answers:** Answers are based on retrieved context and limited to three sentences.
- **Multiple UI Options:** Flask-based web interface and Chainlit interactive chat.
- **Conversation History:** The Chainlit version maintains conversation context for follow-up questions.

## Tech Stack
- Python, Flask, Chainlit
- LangChain, Pinecone, HuggingFace Embeddings
- PDF data ingestion
- HTML/CSS frontend for Flask
- Interactive UI with Chainlit

## Installation

### Prerequisites
- Python 3.8+
- Pinecone API key (for vector search)
- Ollama (for local LLM support)
  - [Install Ollama](https://ollama.ai/download)
  - Pull the llama3 model: `ollama pull llama3:8b`

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/medical-chatbot.git
cd medical-chatbot

# Install dependencies
pip install -r req.txt

# Install Chainlit 
pip install chainlit

# Set up environment variables
# Create a .env file with your Pinecone API key
echo "PINECONE_API_KEY = your_pinecone_api_key" > .env
```

### Index the Medical Data
```bash
python store_index.py
```

### Running the Application

#### Flask UI
```bash
python app_flask.py
```
Visit `http://localhost:5000` in your browser.

#### Chainlit UI
```bash
chainlit run app_cl.py
```
Visit `http://localhost:8000` in your browser.

The application supports two different interfaces:
- **Flask UI**: Classic web interface with HTML/CSS
- **Chainlit UI**: Modern, reactive chat interface with conversation history support

You can customize the Chainlit welcome screen by editing the `chainlit.md` file.

## Folder Structure
```
medical-chatbot/
├── app_flask.py          # Flask app entry point
├── app_cl.py             # Chainlit app entry point (with conversation history)
├── chainlit.md           # Configuration for Chainlit UI
├── store_index.py        # PDF ingestion and vector store
├── req.txt               # Python dependencies
├── setup.py              # Packaging info
├── src/
│   ├── helper.py         # PDF loading, text splitting, embeddings
│   ├── prompt.py         # System prompt for LLM
│   └── __init__.py
├── .chainlit/            # Chainlit configuration directory
├── Data/
│   └── The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf
├── templates/
│   └── chatbot.html      # Frontend HTML for Flask
├── static/
│   └── style.css         # CSS styling for Flask
├── research/
│   └── trials.ipynb      # Research notebook
├── LICENSE
└── README.md
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author
Basil Reda

## Acknowledgements
- [LangChain](https://github.com/langchain-ai/langchain)
- [Pinecone](https://www.pinecone.io/)
- [HuggingFace](https://huggingface.co/)
- [Ollama](https://ollama.ai/)
- [Chainlit](https://chainlit.io/)