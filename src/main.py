from textnode import TextNode, TextType
from htmlnode import *

def main():
    textN = TextNode("hello", TextType.LINK, "www.google.com")
    print(textN)
    
def text_node_to_html_node(test_node):
    if test_node.text_type == TextType.LINK:
        return LeafNode("a", test_node.text, attributes={"href": test_node.url})
    if test_node.text_type == TextType.IMAGE:
        return LeafNode("img", test_node.text, attributes={"src": test_node.url})
    if test_node.text_type == TextType.TEXT:
        return LeafNode(None, test_node.text)
    if test_node.text_type == TextType.BOLD:
        return LeafNode("b", test_node.text)
    if test_node.text_type == TextType.ITALIC:
        return LeafNode("i", test_node.text)
    if test_node.text_type == TextType.CODE:
        return LeafNode("code", test_node.text)
    if test_node.text_type == TextType.BLOCKQUOTE:
        return LeafNode("blockquote", test_node.text)
    if test_node.text_type == TextType.UNDERLINE:
        return LeafNode("u", test_node.text)
    raise ValueError("Invalid TextType")
    
if __name__ == "__main__":
    main()