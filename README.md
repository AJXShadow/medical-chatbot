# Generative AI Medical Chatbot

## Overview
Generative AI Medical Chatbot is an AI-powered virtual assistant designed to provide reliable medical information, preliminary symptom assessment, and healthcare guidance. It leverages large language models and vector search to answer user queries based on a medical encyclopedia PDF.

## Features
- **Symptom Assessment:** Users can describe symptoms and receive possible causes and recommendations.
- **Medical Q&A:** Provides information on conditions, medications, and treatments using LLMs and PDF data.
- **Healthcare Navigation:** Can be extended to help users find healthcare facilities and specialists.
- **Privacy-Focused:** User health data is not stored.
- **Concise, Contextual Answers:** Answers are based on retrieved context and limited to three sentences.

## Tech Stack
- Python, Flask
- LangChain, Pinecone, HuggingFace Embeddings
- PDF data ingestion
- HTML/CSS frontend

## Installation

### Prerequisites
- Python 3.8+
- Pinecone API key (for vector search)

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/medical-chatbot.git
cd medical-chatbot

# Install dependencies
pip install -r req.txt

# Set up environment variables
cp .env.example .env  # or create a .env file manually
# Add your PINECONE_API_KEY to .env
```

### Index the Medical Data
```bash
python store_index.py
```

### Run the Application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Folder Structure
```
medical-chatbot/
├── app.py                # Flask app entry point
├── store_index.py        # PDF ingestion and vector store
├── req.txt               # Python dependencies
├── setup.py              # Packaging info
├── src/
│   ├── helper.py         # PDF loading, text splitting, embeddings
│   ├── prompt.py         # System prompt for LLM
│   └── __init__.py
├── Data/
│   └── The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf
├── templates/
│   └── chatbot.html      # Frontend HTML
├── static/
│   └── style.css         # CSS styling
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