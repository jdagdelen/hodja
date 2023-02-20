"""Unit test for documents.py"""

import unittest
from hodja.search import documents

class TestDocument(unittest.TestCase):
    
    def test_init(self):
        """Test the init method."""
        document = documents.Document(text="test", id=1)
        self.assertEqual(document.text, "test")
        self.assertEqual(document.id, 1)

    def test_eq(self):
        """Test the eq method."""
        document1 = documents.Document(text="test1", id=1)
        document2 = documents.Document(text="test2", id=2)
        document3 = documents.Document(text="test1", id=1)
        self.assertEqual(document1, document3)
        self.assertNotEqual(document1, document2)
    

if __name__ == "__main__":
    unittest.main()