import unittest

from blocknode import *

class TestBlockNode(unittest.TestCase):
    def test_is_quote(self):
        text = "> This is a quote\n> This is another line of the quote"
        self.assertTrue(is_quote(text))
        
    def test_not_is_quote(self):
        text = "> This is a quote\nThis is not a quote"
        self.assertFalse(is_quote(text))
        
    def test_is_unordered_list(self):
        text = "- Item 1\n- Item 2\n- Item 3"
        self.assertTrue(is_unordered_list(text))
        
    def test_not_is_unordered_list(self):
        text = "- Item 1\nItem 2\n- Item 3"
        self.assertFalse(is_unordered_list(text))
        
    def test_is_ordered_list(self):
        text = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertTrue(is_ordered_list(text))
        
    def test_not_is_ordered_list(self):
        text = ". Item 1\nItem 2\n. Item 3"
        self.assertFalse(is_ordered_list(text))
    
    def test_get_block_type_paragraph(self):
        text = "This is a paragraph."
        self.assertEqual(get_block_type(text), BlockType.PARAGRAPH)
        
    def test_get_block_type_heading(self):
        text = "# This is a heading"
        self.assertEqual(get_block_type(text), BlockType.HEADING)
        
    def test_get_block_type_heading2(self):
        text = "## This is a subheading"
        self.assertEqual(get_block_type(text), BlockType.HEADING)
    
    def test_get_block_type_heading_too_long(self):
        text = "####### This is a too long heading"
        self.assertEqual(get_block_type(text), BlockType.PARAGRAPH) 
        
    def test_get_block_type_code(self):
        text = "```python\nprint('Hello, World!')\n```"
        self.assertEqual(get_block_type(text), BlockType.CODE)
        
    def test_get_block_type_ordered_list(self):
        text = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(get_block_type(text), BlockType.ORDERED_LIST)
        
    def test_get_block_type_unordered_list(self):
        text = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(get_block_type(text), BlockType.UNORDERED_LIST)
        
    def test_get_block_type_quote(self):
        text = "> This is a quote\n> This is another line of the quote"
        self.assertEqual(get_block_type(text), BlockType.QUOTE)
        
    def test_get_block_type_empty(self):
        text = ""
        self.assertEqual(get_block_type(text), BlockType.PARAGRAPH)
    