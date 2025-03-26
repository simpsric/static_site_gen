from enum import Enum

class TextType(Enum):
    TEXT = 1
    LINK = 2
    IMAGE = 3
    BOLD = 5
    ITALIC = 6
    CODE = 7
    BLOCKQUOTE = 8
    UNDERLINE = 9
    
class TextNode:
    def __init__(self, text: str, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"