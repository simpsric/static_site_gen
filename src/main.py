from textnode import TextNode, TextType
from htmlnode import *
import re

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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if delimiter in node.text:
            split_text = node.text.split(delimiter)
            for i in range(len(split_text) ):
                if i % 2 == 1:
                    new_nodes.append(TextNode(split_text[i], text_type))
                else:
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    alt_text = re.findall(r"\[.*?\]", text)
    url = re.findall(r"\(.*?\)", text)
    matches = [(t[1:-1], u[1:-1]) for t, u in zip(alt_text, url)]
    return matches

def extract_markdown_links(text):
    alt_text = re.findall(r"\[.*?\]", text)
    url = re.findall(r"\(.*?\)", text)
    matches = [(t[1:-1], u[1:-1]) for t, u in zip(alt_text, url)]
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if "!" in node.text:
            split_text = node.text.split("!")
            max_len = len(split_text)
            len_counter = 0
            while len_counter < max_len:
                if len_counter > 0:
                    if split_text[len_counter][-1] != ")":
                        temp_split = split_text[len_counter].split(" ", maxsplit=1)
                        extract = extract_markdown_images(temp_split[0])
                        new_nodes.append(TextNode(extract[0][0], TextType.IMAGE, extract[0][1]))
                        new_nodes.append(TextNode(" " + temp_split[1], TextType.TEXT))
                    else:
                        extract = extract_markdown_images(split_text[len_counter])
                        new_nodes.append(TextNode(extract[0][0], TextType.IMAGE, extract[0][1]))
                    len_counter += 1
                else:
                    new_nodes.append(TextNode(split_text[len_counter], TextType.TEXT))
                    len_counter += 1
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if "[" in node.text:
            split_text = node.text.split("[")
            max_len = len(split_text)
            len_counter = 0
            while len_counter < max_len:
                if len_counter > 0:
                    if split_text[len_counter][-1] != ")":
                        temp_split = ("[" + split_text[len_counter]).split(" ", maxsplit=1)
                        extract = extract_markdown_links(temp_split[0])
                        new_nodes.append(TextNode(extract[0][0], TextType.LINK, extract[0][1]))
                        new_nodes.append(TextNode(" " + temp_split[1], TextType.TEXT))
                    else:
                        extract = extract_markdown_links("[" + split_text[len_counter])
                        new_nodes.append(TextNode(extract[0][0], TextType.LINK, extract[0][1]))
                    len_counter += 1
                else:
                    new_nodes.append(TextNode(split_text[len_counter], TextType.TEXT))
                    len_counter += 1
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, ">", TextType.BLOCKQUOTE)
    nodes = split_nodes_delimiter(nodes, "__", TextType.UNDERLINE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    
if __name__ == "__main__":
    main()