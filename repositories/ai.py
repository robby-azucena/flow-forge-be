from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_mistralai import MistralAIEmbeddings
from loguru import logger


class AIRepository:
    def __init__(self, embeddings: MistralAIEmbeddings):
        self.embeddings = embeddings

    def create_vector_store(
        self, document: list[Document], collection_name: str = "doc_analysis"
    ) -> Chroma:
        logger.info("Create Vector")
        return Chroma.from_documents(
            documents=document,
            embedding=self.embeddings,
            collection_name=collection_name,
        )

    def retrieve_relevant_documents(
        self,
        vector_store: Chroma,
        question: str,
        k: int = 5,
    ) -> list[Document]:
        logger.info("Retrieve Vector")
        return vector_store.similarity_search(query=question, k=k)

    def delete_vector_store(
        self,
        vector_store: Chroma,
    ) -> None:
        logger.info("Delete Vector")
        vector_store.delete_collection()
