"""Classes for storing and retrieving documents."""
import os
from abc import ABC, abstractmethod
import faiss
import pickle
import json
import numpy as np

class DocStoreBase(ABC):

    @abstractmethod
    def add(self, document):
        """Add a document to the store."""
        pass
    
    @abstractmethod
    def remove(self, document_id):
        """Remove a document from the store."""
        pass

    @abstractmethod
    def get(self, document_id):
        """Get a document from the store."""
        pass

    @abstractmethod
    def get_all(self):
        """Get all documents from the store."""
        pass

    @property
    @abstractmethod
    def __len__(self):
        """Get the number of documents in the store."""
        pass


class DocStore(DocStoreBase):
    """A basic DocStore that stores documents in a dict."""

    def __init__(self):
        self.documents = {}

    def add(self, documents):
        """Add documents to the store.

        Args:
            documents (list): Documents to add to the store.
        """
        for document in documents:
            # check if document has an id, if not, assign one via text hash
            if hasattr(document, "id"):
                # if document has an id, check if it's already in the store
                if document.id in self.documents:
                    raise ValueError(f"Document with id {document.id} already in store.")
                else:
                    self.documents[document.id] = document
            else:
                document.id = hash(document.text)
                self.documents[document.id] = document

    def remove(self, document_ids):
        """Remove documents from the store.

        Args:
            document_ids (list): Document ids to remove from the store.
        """
        for document_id in document_ids:
            del self.documents[document_id]

    def get(self, document_id):
        """Get a document from the store.

        Args:
            document_id: Document id to get from the store.
        """
        return self.documents[document_id]

    def get_all(self):
        """Get all documents from the store."""
        return self.documents.values()

    def __len__(self):
        """Get the number of documents in the store."""
        return len(self.documents)


class VectorStore(DocStoreBase):
    """A DocStore that embeds documents."""

    def __init__(self, embeddings):
        self.embeddings = embeddings
        self.documents = []
        self.document_embeddings = []
        self._ids = []

    def add(self, documents):
        """Get embeddings for documents and add to the vectorstore.

        Args:
            documents: Documents to add to the vectorstore.
        """
        for document in documents:
            # check if document has an id, if not, assign one via text hash
            if hasattr(document, "id"):
                # if document has an id, check if it's already in the vectorstore
                if document.id in self._ids:
                    raise ValueError(f"Document with id {document.id} already in vectorstore.")
                else:
                    self._ids.append(document.id)
            else:
                self._ids.append(hash(document.text))
            self.documents.append(document)
        texts = [document.text for document in documents]
        new_document_embeddings = self.embeddings.embed(texts)
        self.document_embeddings.extend(new_document_embeddings)

    def remove(self, document_ids):
        """Remove documents from the vectorstore.

        Args:
            document_ids (list): Document ids to remove from the vectorstore.
        """
        for document_id in document_ids:
            index = self._ids.index(document_id)
            self.documents = self.documents[:index] + self.documents[index+1:]
            self._ids = self._ids[:index] + self._ids[index+1:]
            self.document_embeddings = self.document_embeddings[:index] + self.document_embeddings[index+1:]

    def get(self, document_id):
        """Get a document from the vectorstore.

        Args:
            document_id: Document id to get from the vectorstore.
        """
        index = self._ids.index(document_id)
        return self.documents[index]

    def get_all(self):
        """Get all documents from the vectorstore."""
        return self.documents

    def __len__(self):
        """Get the number of documents in the vectorstore."""
        return len(self.documents)


class FAISS(VectorStore):
    """Vector database that uses FAISS for fast semantic similarity search over documents."""

    def __init__(self, embeddings, index=None, documents=None):
        super().__init__(embeddings)
        if index is None:
            self.index = faiss.IndexFlatL2(self._embedding_size)
        else:
            self.index = index
        if documents is None:
            self.documents = []
        else:
            self.documents = documents

    @property
    def _embedding_size(self):
        return len(self.embeddings.embed(["dummy"])[0])
        
    def save( self, save_directory):
        """Save to files."""
        faiss.write_index(self.index, "index.faiss")
        with open(os.path.join(save_directory, "documents.json"), "w") as f:
            json.dump(self.documents, f)
        with open(os.path.join(save_directory, "embeddings.pickle"), "wb") as f:
            pickle.dump(self.embeddings, f)

    @classmethod
    def load(cls, save_directory):
        """Load from files."""
        index = faiss.read_index("index.faiss")
        with open(os.path.join(save_directory, "documents.json"), "r") as f:
            documents = json.load(f)
        with open(os.path.join(save_directory, "embeddings.pickle"), "rb") as f:
            embeddings = pickle.load(f)
        return cls(
            embeddings=embeddings,
            index=index,
            documents=documents,
        )

    def add(self, documents):
        """Add documents to the vectorstore.
        
        Args:
            document: Document to add to the vectorstore.
        """
        super().add(documents)
        document_embeddings = self.document_embeddings[-len(documents):]
        document_embeddings = np.array(document_embeddings, dtype=np.float32)
        document_embeddings = document_embeddings.reshape(-1, self._embedding_size)
        self.index.add(document_embeddings)

    def remove(self, document_ids):
        """Remove documents from the vectorstore.
        
        Args:
            document_ids (list): Document ids to remove from the vectorstore.
        """
        super().remove(document_ids)
        self.index = faiss.IndexFlatL2(self._embedding_size)
        self.document_embeddings = np.array(self.document_embeddings, dtype=np.float32)
        if len(self.document_embeddings):
            self.index.add(self.document_embeddings)

    def search(self, query, k=4):
        """Return docs most similar to query."""
        query_embedding = self.embeddings.embed([query])[0]
        query_embedding = np.array(query_embedding, dtype=np.float32)
        D, I = self.index.search(query_embedding.reshape(1, -1), k)
        return [self.documents[i] for i in I[0]]


