import os
import sys
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from rag.exception.exception import RAGException
from rag.logging.logger import logging
from rag.constant import *
from dotenv import load_dotenv
from utils.config import read_yaml

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelLoader:
    """
    A utility class to load embedding models and LLM models for modular RAG systems.
    """

    def __init__(self, config_file_path=CONFIG_FILE_PATH):
        try:
            logger.info(f"Loading config from {config_file_path}")
            self.config = read_yaml(config_file_path)
            load_dotenv()
            self._validate_env()
        except Exception as e:
            logger.error(f"Error initializing ModelLoader: {e}")
            raise

    def _validate_env(self):
        """
        Ensure required environment variables are available.
        """
        required_vars = ["GROQ_API_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            logger.error(f"Missing environment variables: {missing_vars}")
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")

    def load_embeddings(self):
        try:
            """
            Load Hugging Face embeddings for vector store.
            """
            logger.info("Loading Hugging Face embedding model...")
            config = self.config.Model_loader
            model_name = config.model_name
            huggingface_embeddings = HuggingFaceEmbeddings(model_name=model_name)
            logger.info(f"Embedding model {model_name} loaded successfully")
            return huggingface_embeddings
        except RAGException as e:
            logger.error(f"Error loading embeddings: {e}")
            raise

    def load_llm(self):
        try:
            """
            Load LLM via Groq API.
            """
            logger.info("Loading LLM from Groq...")
            config = self.config.Model_loader
            model_name = config.llm_model_name
            llm = ChatGroq(model=model_name, api_key=os.getenv("GROQ_API_KEY"))
            logger.info(f"LLM {model_name} loaded successfully")
            return llm
        except RAGException as e:
            logger.error(f"Error loading LLM: {e}")
            raise

    def run_llm(self):
        try:
            llm = self.load_llm()
            logger.info("Invoking LLM with query: 'What is the capital of France?'")
            result = llm.invoke("What is the capital of India and also tell us history of it?")
            logger.info("LLM invocation successful")
            return result
        except Exception as e:
            logger.error(f"Error invoking LLM: {e}")
            raise

# Run if this file is executed directly
if __name__ == "__main__":
    try:
        loader = ModelLoader()
        loader.load_embeddings
        result = loader.run_llm()
        if hasattr(result, 'content'):
            print(result.content)  # Extract the response content
        else:
            print(result)
    except Exception as e:
        logger.error(f"Error running script: {e}")
        raise