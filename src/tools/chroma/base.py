import chromadb
from chromadb.config import Settings
from typing import List

class ChromaVectorStore:
    def __init__(
        self,
        chroma_db_impl,
        persist_directory,
        collection_name,
        **kwargs
    ) -> None:
        self.client = chromadb.Client(
            Settings(
                chroma_db_impl=chroma_db_impl,
                persist_directory=persist_directory
            )
        )
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(collection_name)
        self.client.persist()
    
    def clear_collection(self):
        self.client.delete_collection(name=self.collection_name)
        self.client.persist()

    def add(self, documents, metadata, ids):
        self.collection.add(documents=documents, metadatas=metadata, ids=ids)
        self.client.persist()

    def query(self, query_texts, n_results):
        results = self.collection.query(
            query_texts=query_texts,
            n_results=n_results,
        )
        # TODO: return ids and others necessary
        return results

    def query_from_specific_entitys(self, entity_types: List[str]):
        # TODO: unimplement
        raise NotImplementedError