import getpass
import os
import sys
import time
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
from typing import List
from rag.exception.exception import RAGException
from rag.logging.logger import logging
from rag.constant import *
from utils.config import read_yaml
from rag.model_loaders.model_loader import ModelLoader
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from pinecone import Pinecone, ServerlessSpec



class DataIngestion:
    def __init__(self,config_file_path=CONFIG_FILE_PATH):
        self.config=read_yaml(config_file_path)
        self.model_loader=ModelLoader()
        self.csv_path=self._get_csv_path()
        self.product_data=self._load_csv()
        self.embeddings=self.model_loader.load_embeddings()

    def _get_csv_path(self):
        try:
            """
            Get path to the CSV file located inside 'data' folder.
            """
            current_dir = os.getcwd()
            csv_path = os.path.join(current_dir, 'data', 'flipkart_product_review.csv')

            if not os.path.exists(csv_path):
                raise FileNotFoundError(f"CSV file not found at: {csv_path}")

            return csv_path 
        except RAGException as e:
            raise (f"Error getting CSV path: {e,sys}")  

    def _load_csv(self):
        try:
            """
            Load product data from CSV.
            """
            df = pd.read_csv(self.csv_path)
            expected_columns = {'product_title', 'rating', 'summary', 'review'}

            if not expected_columns.issubset(set(df.columns)):
                raise ValueError(f"CSV must contain columns: {expected_columns}")

            return df 
        except RAGException as e:
            raise (f"Error loading CSV: {e,sys}")

    def transform_data(self):
        try:
            """
            Transform product data into list of LangChain Document objects.
            """
            product_list = []

            for _, row in self.product_data.iterrows():
                product_entry = {
                    "product_name": row['product_title'],
                    "product_rating": row['rating'],
                    "product_summary": row['summary'],
                    "product_review": row['review']
                }
                product_list.append(product_entry)

            documents = []
            for entry in product_list:
                metadata = {
                    "product_name": entry["product_name"],
                    "product_rating": entry["product_rating"],
                    "product_summary": entry["product_summary"]
                }
                doc = Document(page_content=entry["product_review"], metadata=metadata)
                documents.append(doc)

            print(f"Transformed {len(documents)} documents.")
            return documents
        except RAGException as e:
            raise (f"Error transforming data: {e,sys}")
    
    def vector_store(self,documents: List[Document]):
        ''' storing the data in vector store '''
        try:
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
            vector_store = PineconeVectorStore(index=index, embedding=embeddings)
            inserted_ids=vector_store.add_documents(documents)
            return vector_store, inserted_ids

        except RAGException as e:
            raise (f"Error storing data in vector store: {e,sys}")
        
    
    def run_pipeline(self):
        """
        Run the full data ingestion pipeline: transform data and store into vector DB.
        """
        documents = self.transform_data()
        vstore, inserted_ids = self.vector_store(documents)

        # Optionally do a quick search
        query = "Can you tell me the low budget headphone?"
        results = vstore.similarity_search(query)

        print(f"\nSample search results for query: '{query}'")
        for res in results:
            print(f"Content: {res.page_content}\nMetadata: {res.metadata}\n")

# Run if this file is executed directly
if __name__ == "__main__":
    ingestion = DataIngestion()
    ingestion.run_pipeline()




# import os
# import sys
# import time
# import pandas as pd
# from hashlib import md5
# from typing import List
# from dotenv import load_dotenv

# from rag.exception.exception import RAGException
# from rag.logging.logger import logging
# from rag.constant import *
# from utils.config import read_yaml
# from rag.model_loaders.model_loader import ModelLoader

# from langchain_core.documents import Document
# from langchain_pinecone import PineconeVectorStore
# from pinecone import Pinecone, ServerlessSpec

# load_dotenv()


# class DataIngestion:
#     def __init__(self, config_file_path=CONFIG_FILE_PATH):
#         self.config = read_yaml(config_file_path)
#         self.model_loader = ModelLoader()
#         self.csv_path = self._get_csv_path()
#         self.product_data = self._load_csv()
#         self.embeddings = self.model_loader.load_embeddings()

#     def _get_csv_path(self):
#         try:
#             current_dir = os.getcwd()
#             csv_path = os.path.join(current_dir, 'data', 'flipkart_product_review.csv')
#             if not os.path.exists(csv_path):
#                 raise FileNotFoundError(f"CSV file not found at: {csv_path}")
#             return csv_path
#         except Exception as e:
#             raise RAGException(f"Error getting CSV path: {e}", sys)

#     def _load_csv(self):
#         try:
#             df = pd.read_csv(self.csv_path)
#             expected_columns = {'product_title', 'rating', 'summary', 'review'}
#             if not expected_columns.issubset(set(df.columns)):
#                 raise ValueError(f"CSV must contain columns: {expected_columns}")
#             return df
#         except Exception as e:
#             raise RAGException(f"Error loading CSV: {e}", sys)

#     def transform_data(self) -> List[Document]:
#         try:
#             product_list = []
#             for _, row in self.product_data.iterrows():
#                 product_entry = {
#                     "product_name": row['product_title'],
#                     "product_rating": row['rating'],
#                     "product_summary": row['summary'],
#                     "product_review": row['review']
#                 }
#                 product_list.append(product_entry)

#             documents = []
#             for entry in product_list:
#                 content = entry["product_review"]
#                 unique_id = md5(content.encode('utf-8')).hexdigest()
#                 metadata = {
#                     "id": unique_id,
#                     "product_name": entry["product_name"],
#                     "product_rating": entry["product_rating"],
#                     "product_summary": entry["product_summary"]
#                 }
#                 doc = Document(page_content=content, metadata=metadata)
#                 documents.append(doc)

#             print(f"Transformed {len(documents)} documents.")
#             return documents
#         except Exception as e:
#             raise RAGException(f"Error transforming data: {e}", sys)

#     def vector_store(self, documents: List[Document]):
#         try:
#             config = self.config.data_ingestion
#             pinecone_api_key = os.environ.get("PINECONE_API_KEY")
#             pc = Pinecone(api_key=pinecone_api_key)
#             index_name = config.index_name
#             existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

#             if index_name not in existing_indexes:
#                 pc.create_index(
#                     name=index_name,
#                     dimension=config.dimension,
#                     metric=config.metric,
#                     spec=ServerlessSpec(cloud=config.cloud, region=config.region),
#                 )
#                 while not pc.describe_index(index_name).status[config.status]:
#                     time.sleep(1)

#             index = pc.Index(index_name)
#             vector_store = PineconeVectorStore(index=index, embedding=self.embeddings)

#             new_docs = []
#             new_ids = []

#             for doc in documents:
#                 doc_id = doc.metadata["id"]
#                 # Check if doc_id exists in Pinecone
#                 existing = index.fetch(ids=[doc_id])
#                 if not existing.vectors:
#                     new_docs.append(doc)
#                     new_ids.append(doc_id)

#             if new_docs:
#                 inserted_ids = vector_store.add_documents(new_docs, ids=new_ids)
#                 print(f"Inserted {len(inserted_ids)} new documents.")
#             else:
#                 print("All documents already exist in the vector store.")

#             return vector_store, new_ids
#         except Exception as e:
#             raise RAGException(f"Error storing data in vector store: {e}", sys)

#     def run_pipeline(self):
#         documents = self.transform_data()
#         vstore, inserted_ids = self.vector_store(documents)

#         if vstore and inserted_ids:
#             query = "Can you tell me the low budget headphone?"
#             results = vstore.similarity_search(query)

#             print(f"\nSample search results for query: '{query}'")
#             for res in results:
#                 print(f"Content: {res.page_content}\nMetadata: {res.metadata}\n")


# if __name__ == "__main__":
#     ingestion = DataIngestion()
#     ingestion.run_pipeline()
