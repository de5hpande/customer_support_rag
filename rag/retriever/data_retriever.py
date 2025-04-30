import os
import sys
import time
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from rag.model_loaders.model_loader import ModelLoader
from utils.config import read_yaml
from rag.exception.exception import RAGException
from rag.logging.logger import logging
from langchain_core.documents import Document
from typing import List
from rag.constant import CONFIG_FILE_PATH
from dotenv import load_dotenv
load_dotenv()

class DataRetriever:
    """retrieving data from vector store"""
    def __init__(self,config_file_path=CONFIG_FILE_PATH):
        self.config=read_yaml(config_file_path)
        self.model_loader=ModelLoader()
        self.embeddings=self.model_loader.load_embeddings()
        self.vstore = None
        self.retriever = None

    def load_retriever(self):
        if not self.vstore:
            config=self.config.data_ingestion

            pinecone_api_key = os.environ.get("PINECONE_API_KEY")
            pc = Pinecone(api_key=pinecone_api_key)
            index_name = config.index_name
            existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

            if index_name not in existing_indexes:
                pc.create_index(
                    name=index_name,
                    dimension=config.dimension,
                    metric=config.metric,
                    spec=ServerlessSpec(cloud=config.cloud, region=config.region),
                )
                while not pc.describe_index(index_name).status[config.status]:
                    time.sleep(1)
                
            index = pc.Index(index_name)
            embeddings = self.embeddings
            self.vstore = PineconeVectorStore(index=index, embedding=embeddings)

        if not self.retriever:
            top_k =4
            retriever = self.vstore.as_retriever(search_kwargs={"k": top_k})
            print("Retriever loaded successfully.")
            return retriever
    
    def call_retriever(self,query:str)-> List[Document]:
        retriever=self.load_retriever()
        output=retriever.invoke(query)
        return output

    
if __name__=='__main__':
    retriever_obj = DataRetriever()
    user_query = "Can you suggest good budget laptops?"
    results = retriever_obj.call_retriever(user_query)

    for idx, doc in enumerate(results, 1):
        print(f"Result {idx}: {doc.page_content}\nMetadata: {doc.metadata}\n")