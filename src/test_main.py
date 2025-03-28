import unittest

from main import *

class TestMain(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_delimiter(self):
        node = TextNode("This is a !text! node", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "!", TextType.CODE)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text, " node")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        
    def test_codeDelim(self):
        node = TextNode("This is a `text` node", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text, " node")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
    
    def test_noDelim(self):
        node = TextNode("This is a text node", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "!", TextType.CODE)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is a text node")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        
    def test_multDelim(self):
        node = TextNode("This is a !text! node with an extra !text! portion", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "!", TextType.CODE)
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text, "This is a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text, " node with an extra ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "text")
        self.assertEqual(nodes[3].text_type, TextType.CODE)
        self.assertEqual(nodes[4].text, " portion")
        
    def test_extractMd_images(self):
        text = "![alt text](www.google.com)"
        nodes = extract_markdown_images(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0][0], "alt text")
        self.assertEqual(nodes[0][1], "www.google.com")
        
    def test_extractMd_images_more(self):
        text = "![alt text](www.google.com) ![alt text](www.google.com)"
        nodes = extract_markdown_images(text)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0][0], "alt text")
        self.assertEqual(nodes[0][1], "www.google.com")
        self.assertEqual(nodes[1][0], "alt text")
        self.assertEqual(nodes[1][1], "www.google.com")
        
    def test_extractMd_links(self):
        text = "[alt text](www.google.com)"
        nodes = extract_markdown_links(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0][0], "alt text")
        self.assertEqual(nodes[0][1], "www.google.com")
        
    def test_extractMd_links_more(self):
        text = "[alt text](www.google.com) [alt text](www.google.com)"
        nodes = extract_markdown_links(text)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0][0], "alt text")
        self.assertEqual(nodes[0][1], "www.google.com")
        self.assertEqual(nodes[1][0], "alt text")
        self.assertEqual(nodes[1][1], "www.google.com")
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.google.com"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links_no_text(self):
        node = TextNode(
            "[link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )
    
    def test_split_links_no_text_end(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )
        
    def test_split_links_no_text_start(self):
        node = TextNode(
            "[link](https://www.google.com) and another",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_split_links_no_text_start_end(self):
        node = TextNode(
            "[link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )
        
    def test_text_to_textnodes(self):
        text = "This is a **text** node with a *link* and an `image`"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 7)
        self.assertEqual(nodes[0].text, "This is a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " node with a ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "link")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " and an ")
        self.assertEqual(nodes[4].text_type, TextType.TEXT)
        self.assertEqual(nodes[5].text, "image")
        self.assertEqual(nodes[5].text_type, TextType.CODE)
        self.assertEqual(nodes[6].text, "")
        self.assertEqual(nodes[6].text_type, TextType.TEXT)
        