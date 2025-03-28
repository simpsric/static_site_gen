import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")
    def test_repr_link(self):
        node = TextNode("This is a text node", TextType.LINK, "www.google.com")
        self.assertEqual(repr(node), "TextNode(This is a text node, link, www.google.com)")
    def test_neq_url(self):
        node = TextNode("This is a text node", TextType.LINK, "www.google.com")
        node2 = TextNode("This is a text node", TextType.LINK, "www.google.com")
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()