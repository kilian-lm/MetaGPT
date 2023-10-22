## api_chunker.py
from typing import List

class ApiChunker:
    def __init__(self, chunk_size: int = 500):
        self.chunk_size = chunk_size

    def chunk_text(self, text: str) -> List[str]:
        """
        Splits the text into chunks of the specified size.
        """
        return [text[i:i+self.chunk_size] for i in range(0, len(text), self.chunk_size)]
