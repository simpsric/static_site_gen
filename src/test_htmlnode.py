import unittest

from htmlnode import *


class TestHtmlNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("p", "This is a paragraph")
        self.assertRaises(NotImplementedError, node.to_html)
        
    def test_props_to_html(self):
        node = HTMLNode("p", "This is a paragraph", attributes={"class": "paragraph"})
        self.assertEqual(node.props_to_html(), ' class="paragraph"')
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    


if __name__ == "__main__":
    unittest.main()