# 🤖 Customer Support RAG System

A Retrieval-Augmented Generation (RAG) based customer support system that uses advanced NLP techniques to provide accurate and contextually relevant responses to customer queries.

## 📋 Project Overview

This project implements a customer support chatbot using RAG architecture. It retrieves relevant information from product reviews to answer customer questions about products, features, issues, and more.

## ✨ Features

- 🔍 Natural language query processing
- 📊 Context-aware responses using product review data
- 💾 Memory to maintain conversation context
- 🌐 Web-based chat interface
- 📝 Logging and exception handling
- ⚙️ Configurable components

## 🛠️ Tech Stack

- **Python**: Core programming language
- **FastAPI**: Web framework for API
- **LangChain**: Framework for LLM applications
- **Pinecone**: Vector database for similarity search
- **Groq**: LLM provider
- **Pandas**: Data manipulation and analysis
- **UV**: Package manager and installer
- **Jinja2**: Templating engine for HTML
- **HuggingFace**: For embeddings and models

## 📁 Project Structure

```
└── customer_support_rag/
    ├── README.md
    ├── main.py                    # FastAPI application entry point
    ├── pyproject.toml             # Project metadata and dependencies
    ├── requirements.txt           # Project dependencies
    ├── uv.lock                    # UV lock file
    ├── .python-version            # Python version specification
    ├── config/                    # Configuration files
    │   └── config.yaml
    ├── data/                      # Data files
    │   └── flipkart_product_review.csv
    ├── logs/                      # Log files
    ├── notebook/                  # Jupyter notebooks for experimentation
    │   └── customer_service_bot.ipynb
    ├── rag/                       # Core RAG modules
    │   ├── __init__.py
    │   ├── constant/
    │   ├── data_ingestion/
    │   ├── exception/
    │   ├── logging/
    │   ├── model_loaders/
    │   ├── model_with_memory/
    │   ├── prompts/
    │   └── retriever/
    ├── static/                    # Static assets for web interface
    │   └── style.css
    ├── templates/                 # HTML templates
    │   └── chat.html
    └── utils/                     # Utility functions
        ├── __init__.py
        └── config.py
```

## 🚀 Setup and Installation

### Prerequisites

- Python 3.9+
- [UV](https://github.com/astral-sh/uv) package manager

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/customer_support_rag.git
   cd customer_support_rag
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Using UV to install dependencies
   uv pip install -r requirements.txt
   ```

3. Create a `.env` file with your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENVIRONMENT=your_pinecone_environment
   ```

## 🏃‍♂️ Running the Application

Run the FastAPI server:
```bash
uvicorn main:app --reload --port 8001
```

Access the web interface at: http://localhost:8001

## 📊 Data Flow

1. Customer query is received via the web interface
2. Query is processed and embedded
3. Relevant context is retrieved from product reviews
4. LLM generates a response using the retrieved context
5. Response is displayed to the user

## 🧩 Components

### Data Ingestion
- Loads and processes product review data
- Creates vector embeddings for efficient retrieval

### Retriever
- Performs vector similarity search to find relevant reviews
- Formats context for the LLM

### Memory
- Maintains conversation history
- Provides context for follow-up questions

### Model Loader
- Initializes and configures LLM models
- Manages API connections

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

For any questions or support, please reach out to [your-email@example.com](mailto:your-email@example.com).
