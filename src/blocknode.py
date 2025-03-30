from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"
    QUOTE = "quote"
    
def is_quote(text):
    if not text:
        return False
    for line in text.splitlines():
        if not line.startswith(">"):
            return False
    return True

def is_unordered_list(text):
    if not text:
        return False
    for line in text.splitlines():
        if not line.startswith("- "):
            return False
    return True

def is_ordered_list(text):
    if not text:
        return False
    for line in text.splitlines():
        if not re.match(r"^\d+\.\s", line):
            return False
    return True
    
def get_block_type(text):
    if re.match(r"^#{1,6} ", text):
        return BlockType.HEADING
    elif is_unordered_list(text):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(text):
        return BlockType.ORDERED_LIST
    elif is_quote(text):
        return BlockType.QUOTE
    elif text.startswith("```") and text.endswith("```"):
        return BlockType.CODE
    else:
        return BlockType.PARAGRAPH
