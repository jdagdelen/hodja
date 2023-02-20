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


class DocStore(DocStoreBase):
    """A basic DocStore that stores documents in a dict."""

    def __init__(self):
        self.documents = {}

    def add(self, document):
        """Add a document to the store.

        Args:
            document: Document to add to the store.
        """
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

    def remove(self, document_id):
        """Remove a document from the store.

        Args:
            document_id: Document id to remove from the store.
        """
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


class VectorStore(DocStoreBase):
    """A DocStore that embeds documents."""

    def __init__(self, embedding_function):
        self.embedding_function = embedding_function
        self.documents = []
        self.embeddings = []
        self._ids = []

    def add(self, document):
        """Run a document through the embedding_function and add to the vectorstore.

        Args:
            document: Document to add to the vectorstore.
        """
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
        embedding = self.embedding_function([document.text])[0]
        self.embeddings.append(embedding)

    def remove(self, document_id):
        """Remove a document from the vectorstore.

        Args:
            document_id: Document id to remove from the vectorstore.
        """
        index = self._ids.index(document_id)
        self.documents = self.documents[:index] + self.documents[index+1:]
        self.embeddings = self.embeddings[:index] + self.embeddings[index+1:]
        self._ids = self._ids[:index] + self._ids[index+1:]

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


class FAISS(VectorStore):
    """Vector database that uses FAISS for fast semantic similarity search over documents."""

    def __init__(self, embedding_function, index=None, documents=None):
        super().__init__(embedding_function)
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
        return len(self.embedding_function(["dummy"])[0])
        
    def save( self, save_directory):
        """Save to files."""
        faiss.write_index(self.index, "index.faiss")
        with open(os.path.join(save_directory, "documents.json"), "w") as f:
            json.dump(self.documents, f)
        with open(os.path.join(save_directory, "embedding_function.pickle"), "wb") as f:
            pickle.dump(self.embedding_function, f)

    @classmethod
    def load(cls, save_directory):
        """Load from files."""
        index = faiss.read_index("index.faiss")
        with open(os.path.join(save_directory, "documents.json"), "r") as f:
            documents = json.load(f)
        with open(os.path.join(save_directory, "embedding_function.pickle"), "rb") as f:
            embedding_function = pickle.load(f)
        return cls(
            embedding_function=embedding_function,
            index=index,
            documents=documents,
        )

    def add(self, document):
        """Add a document to the vectorstore."""
        super().add(document)
        embedding = self.embeddings[-1]
        embedding = np.array(embedding, dtype=np.float32)
        self.index.add(embedding.reshape(1, -1))

    def remove(self, document_id):
        """Remove a document from the vectorstore."""
        super().remove(document_id)
        # Have to rebuild FAISS index each time after removing a document
        # This isn't ideal, maybe there's a better way?
        self.index = faiss.IndexFlatL2(self._embedding_size)
        self.embeddings = np.array(self.embeddings, dtype=np.float32)
        self.index.add(self.embeddings)

    def search(self, query, k=4):
        """Return docs most similar to query."""
        query_embedding = self.embedding_function([query])[0]
        query_embedding = np.array(query_embedding, dtype=np.float32)
        D, I = self.index.search(query_embedding.reshape(1, -1), k)
        print(self.documents)
        return [self.documents[i] for i in I[0]]


