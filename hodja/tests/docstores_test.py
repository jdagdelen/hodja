"""Unit tests for the docstores module."""

import unittest

from hodja.search import docstores
from hodja.search.documents import Document

class TestDocstore(unittest.TestCase):
    """Unit tests for the DocStore class."""

    def test_add(self):
        """Test the add method."""
        store = docstores.DocStore()
        document = Document(text="test", id=1)
        store.add([document])
        self.assertEqual(store.documents, {hash(document.id): document})

    def test_remove(self):
        """Test the remove method."""
        store = docstores.DocStore()
        document1 = Document(text="test1", id=1)
        document2 = Document(text="test2", id=2)
        documents = [document1, document2]
        store.add(documents)
        store.remove([document1.id])
        self.assertEqual(store.documents, {document2.id: document2})

    def test_get(self):
        """Test the get method."""
        store = docstores.DocStore()
        document1 = Document(text="test1", id=1)
        document2 = Document(text="test2", id=2)
        documents = [document1, document2]
        store.add(documents)
        self.assertEqual(store.get(document1.id), document1)

def cond(text):
        if "3" in text:
            return [0, 0, 0]
        else:
            return [1, 1, 1]
            
def dummy_embedding_function(text):
    if not isinstance(text, list):
        text = [text]
    embeddings = [cond(t) for t in text]
    return embeddings

class DummyEmbeddings:
    def __init__(self):
        self.embedding_function = dummy_embedding_function

    def embed(self, docs):
        return dummy_embedding_function(docs)

class TestFAISS(unittest.TestCase):

    def test_add(self):
        """Test the add method."""
        store = docstores.FAISS(DummyEmbeddings())
        document = Document(text="test", id=1)
        store.add([document])
        self.assertEqual(store.documents, [document])

    def test_remove(self):
        """Test the remove method."""
        store = docstores.FAISS(DummyEmbeddings())
        document1 = Document(text="test1", id=1)
        document2 = Document(text="test2", id=2)
        documents = [document1, document2]
        store.add(documents)
        store.remove([document1.id])
        self.assertEqual(store.documents, [document2])

    def test_get(self):
        """Test the get method."""
        store = docstores.FAISS(DummyEmbeddings())
        document1 = Document(text="test1", id=1)
        document2 = Document(text="test2", id=2)
        documents = [document1, document2]
        store.add(documents)
        self.assertEqual(store.get(document1.id), document1)

    def test_get_all(self):
        """Test the get_all method."""
        store = docstores.FAISS(DummyEmbeddings())
        document1 = Document(text="test1", id=1)
        document2 = Document(text="test2", id=2)
        documents = [document1, document2]
        store.add(documents)
        self.assertEqual(store.get_all(), [document1, document2])
    
    def test_search(self):
        """Test the search method."""
        store = docstores.FAISS(DummyEmbeddings())
        document1 = Document(text="test1", id=1)
        document2 = Document(text="test2", id=2)
        document3 = Document(text="test3", id=3)
        documents = [document1, document2, document3]
        store.add(documents)
        self.assertEqual(store.search(document3.text, 1), [document3])

if __name__ == '__main__':
    unittest.main()