from textnode import TextNode, TextType
from htmlnode import *
from blocknode import *
import re, os, shutil, sys

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
    if test_node.text_type == TextType.HEADING:
        return LeafNode("h1", test_node.text)
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
            split_text = re.split(r'(!\[.*?\]\(.*?\))', node.text)
            max_len = len(split_text)
            for text in split_text:
                extracted = extract_markdown_images(text)
                if extracted:
                    new_nodes.append(TextNode(extracted[0][0], TextType.IMAGE, extracted[0][1]))
                else:
                    new_nodes.append(TextNode(text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if "[" in node.text:
            split_text = re.split(r'(\[.*?\]\(.*?\))', node.text)
            for text in split_text:
                extracted = extract_markdown_links(text)
                if extracted:
                    new_nodes.append(TextNode(extracted[0][0], TextType.LINK, extracted[0][1]))
                else:
                    new_nodes.append(TextNode(text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, ">", TextType.BLOCKQUOTE)
    nodes = split_nodes_delimiter(nodes, "__", TextType.UNDERLINE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(text):
    blocks = [i.strip('\n').strip() for i in text.split("\n\n")]
    new_blocks = []
    for block in blocks:
        if len(block) == 0:
            continue
        new_blocks.append(block)
    return new_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = get_block_type(block)
        match(block_type):
            case BlockType.PARAGRAPH:
                block = ' '.join(block.split("\n"))
                text_nodes = text_to_textnodes(block)
                temp_list = []
                for node in text_nodes:
                    temp_list.append(text_node_to_html_node(node))
                tmp_par = ParentNode("p", temp_list)
                html_nodes.append(tmp_par)
            case BlockType.HEADING:
                header_type = len(block.split(" ", maxsplit=1)[0])
                block = '\n'.join([i.split("# ")[1].strip() for i in block.split("\n")])
                text_nodes = text_to_textnodes(block)
                tmp_list = []
                for node in text_nodes:
                    tmp_list.append(text_node_to_html_node(node))
                match header_type:
                    case 1:
                        html_nodes.append(ParentNode("h1", tmp_list))
                    case 2:
                        html_nodes.append(ParentNode("h2", tmp_list))
                    case 3:
                        html_nodes.append(ParentNode("h3", tmp_list))
                    case 4:
                        html_nodes.append(ParentNode("h4", tmp_list))
                    case 5:
                        html_nodes.append(ParentNode("h5", tmp_list))
                    case 6:
                        html_nodes.append(ParentNode("h6", tmp_list))
                    case _:
                        raise ValueError("Invalid header type")
            case BlockType.CODE:
                block = block[3:-3].strip() + "\n"
                html_nodes.append(LeafNode("pre",LeafNode("code", block).to_html()))
            case BlockType.ORDERED_LIST:
                new_block = ''
                for bl in block.split("\n"):
                    if bl == "":
                        continue
                    bl = bl.split(". ")[1].strip()
                    tmp_text = text_to_textnodes(bl)
                    tmp_lst = []
                    for node in tmp_text:
                        tmp_lst.append(text_node_to_html_node(node))
                    new_block += ParentNode("li", tmp_lst).to_html()
                new_block = LeafNode("ol", new_block)
                html_nodes.append(new_block)
            case BlockType.UNORDERED_LIST:
                new_block = ''
                for bl in block.split("\n"):
                    if bl == "":
                        continue
                    bl = bl.strip("- ")
                    tmp_text = text_to_textnodes(bl)
                    tmp_lst = []
                    for node in tmp_text:
                        tmp_lst.append(text_node_to_html_node(node))
                    new_block += ParentNode("li", tmp_lst).to_html()
                new_block = LeafNode("ul", new_block)
                html_nodes.append(new_block)
            case BlockType.QUOTE:
                block = '\n'.join([i.split('>')[1].strip() for i in block.split("\n")])
                html_nodes.append(LeafNode("blockquote", block))
            case _:
                raise ValueError("Invalid BlockType")
    html_parent = ParentNode("div", html_nodes)
    return html_parent

def copy_file(src, dst, file):
    if not os.path.isfile(os.path.join(src, file)):
        os.makedirs(os.path.join(dst, file), exist_ok=True)
        for item in os.listdir(os.path.join(src, file)):
            copy_file(os.path.join(src, file), os.path.join(dst, file), item)
    else:
        shutil.copy(os.path.join(src, file), os.path.join(dst, file))

def clean_and_copy_static(src, dst):
    src_dir = os.path.join(os.getcwd(), src)
    dest_dir = os.path.join(os.getcwd(), dst)
    shutil.rmtree(dest_dir, ignore_errors=True)
    os.makedirs(dest_dir, exist_ok=True)
    for item in os.listdir(src_dir):
        copy_file(src_dir, dest_dir, item)
        
def extract_title(markdown):
    title = re.findall(r"# (.*)", markdown)
    if title:
        return title[0].strip(), markdown.replace("# " + title[0], "").strip()
    raise Exception("No title found in markdown")

def verify_and_make_dir(path, dst_path):
    print(os.path.dirname(path))
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path), exist_ok=True)

def generate_page(basepath, from_path, template_path, dest_path):
    print("Generating HTML page...")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    title, content = extract_title(markdown)
    html_content = markdown_to_html_node(markdown).to_html()
    html_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    html_page = html_page.replace('href="/', 'href="{BASEPATH}')
    html_page = html_page.replace('src="/', 'src="{BASEPATH}')
    html_page = html_page.replace("{BASEPATH}", basepath)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(html_page)
    print("HTML page generated successfully.")
    
def generate_pages(basepath, dire_path_content, template_path, dest_dir_path):
    print("Generating HTML pages...")
    for root, dirs, files in os.walk(dire_path_content):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                dest_path = os.path.join(dest_dir_path, os.path.relpath(full_path, dire_path_content)).replace(".md", ".html")
                generate_page(basepath, full_path, template_path, dest_path)
    print("HTML pages generated successfully.")
    
if __name__ == "__main__":
    basepath = '/'
    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    elif len(sys.argv) > 3:
        print("Usage: python3 main.py or python3 main.py <basepath>")
        exit(1)
    clean_and_copy_static("static", "docs")
    generate_pages(basepath, "content", "src/template.html", "docs")