from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from rag.prompts.prompt import PROMPT_TEMPLATES, RETRIEVER_PROMPT
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from rag.model_loaders.model_loader import ModelLoader
from rag.retriever.data_retriever import DataRetriever

# Global store for session chat history
store = {}

class ChatHistory:
    def __init__(self):
        self.model_loader = ModelLoader()
        self.retriever = DataRetriever()

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]

    def chain(self):
        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", RETRIEVER_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ])
        
        history_aware_retriever = create_history_aware_retriever(
            self.model_loader.load_llm(),
            self.retriever.load_retriever(),
            contextualize_q_prompt
        )
        
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", PROMPT_TEMPLATES),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        question_answer_chain = create_stuff_documents_chain(
            self.model_loader.load_llm(), qa_prompt
        )
        
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        return rag_chain

    def get_response(self, query: str, session_id: str) -> str:
        rag_chain = self.chain()

        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        result = conversational_rag_chain.invoke(
            {"input": query},
            config={"configurable": {"session_id": session_id}},
        )

        return result["answer"]

# if __name__ == "__main__":
#     chathistory= ChatHistory()
#     session_id = "session_1"
#     query="show me best headphones"
#     response = chathistory.get_response(query, session_id)
#     print(response)