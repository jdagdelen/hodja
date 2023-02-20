from abc import ABC, abstractmethod

class DocumentBase(ABC):
    """A basic document, which is just a string."""

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return f"Document({self.text})"

    def __repr__(self):
        return self.text



class Document(DocumentBase):
    
    def __init__(self, text, **kwargs):
        """A document."""
        super().__init__(text)
        self.__dict__.update(kwargs)

    def __str__(self):
        return f"Document({self.text}, {self.__dict__})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
