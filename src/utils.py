import re
import os
import shutil

from typing import List, Tuple
from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import ParentNode, HTMLNode, LeafNode
from blocktypes import BlockType, block_to_block_type

def split_nodes_delimiter(old_nodes: List, delimiter: str, text_type: TextType) -> List:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text: str) -> List[Tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> List[Tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    images = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            images.append(node)
            continue
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            images.append(TextNode(node.text, TextType.TEXT))
            continue
        for match in matches:
            image_index_start = node.text.find(match[0])
            image_index_end = node.text.find(match[1])
            
            images.append(TextNode(node.text[:image_index_start - 2], TextType.TEXT))
            if image_index_end > -1:
                images.append(TextNode(match[0], TextType.IMAGE, match[1]))
            node.text = node.text[image_index_end + len(match[1]) + 1:]
        if node.text != "":
            images.append(TextNode(node.text, TextType.TEXT))
        
    return images

def split_nodes_link(old_nodes):
    link_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            link_nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            link_nodes.append(node)
            continue
        for match in matches:
            image_index_start = node.text.find(match[0])
            image_index_end = node.text.find(match[1])
            link_nodes.append(TextNode(node.text[:image_index_start - 1], TextType.TEXT))
            if image_index_end > -1:
                link_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            node.text = node.text[image_index_end + len(match[1]) + 1:]
        if node.text != "":
            link_nodes.append(TextNode(node.text, TextType.TEXT))
    return link_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown: str) -> List[str]:
    blocks = []
    split_md = markdown.split("\n\n")
    for block in split_md:
        if block == "":
            continue
        blocks.append(block.strip())
    return blocks

def markdown_to_html_node(markdown: str) -> ParentNode:
    '''Converts full Markdown Document to a Single HTMLNode parent'''
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match(block_type):
            case (BlockType.HEADING):
                children.append(convert_header_block_to_html(block))
            case (BlockType.CODE):
                children.append(convert_code_block_to_html(block))
            case (BlockType.QUOTE):
                children.append(convert_quote_block_to_html(block))
            case (BlockType.PARAGRAPH):
                children.append(convert_paragraph_block_to_html(block))
            case (BlockType.UNORDERED_LIST):
                children.append(convert_unord_block_to_html(block))
            case (BlockType.ORDERED_LIST):
                children.append(convert_ord_block_to_html(block))

            case _:
                raise Exception(f"invalid block: {block_type}")

    return ParentNode("div", children, None) 

def convert_text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children

def convert_header_block_to_html(block):
    # <h1-6>
    count = 0
    for i in block:
        if i == "#":
            count += 1
    node = LeafNode(f"h{count}", block[count+1:])
    return node 

def convert_code_block_to_html(block: str):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def convert_quote_block_to_html(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = convert_text_to_children(content)
    return ParentNode("blockquote", children)

def convert_paragraph_block_to_html(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = convert_text_to_children(paragraph)
    return ParentNode("p", children)

def convert_unord_block_to_html(block):
    html_nodes = []
    block = block.split('\n')
    for item in block:
        text = item[2:]
        children = convert_text_to_children(text) 
        html_nodes.append(ParentNode('li', children))
    return ParentNode("ul", html_nodes)

def convert_ord_block_to_html(block):
    html_nodes = []
    block = block.split("\n")
    for item in block:
        text = item[3:]
        children = convert_text_to_children(text)
        html_nodes.append(ParentNode("li", children))
    return ParentNode("ol", html_nodes)

def copy_dir_to_dest(from_dir, dest_dir):
    if not os.path.exists(from_dir):
        raise ValueError(f"Source directory does not exist: {from_dir}")

    if os.path.exists(dest_dir):
        print(f"Removing files from {dest_dir} folder...")
        shutil.rmtree(dest_dir)

    print(f"The destination directory {dest_dir} does not exist...")
    print(f"Creating {dest_dir} via mkdir")
    os.makedirs(dest_dir)
    
    print(f"Attempting to move files from {from_dir} to {dest_dir}...")
    print(f"Copying Files from {from_dir}...")
    copy_files = os.listdir(from_dir)
    for file in copy_files:
        file_path = os.path.join(from_dir, file)
        copy_files_recursive(file_path, dest_dir)

def copy_files_recursive(source, dest):
    if os.path.isfile(source):
        print(f"Copying file {source} to {dest}...")
        shutil.copy(source, dest)
        return
    
    dest_dir = os.path.join(dest, os.path.basename(source))
    if not os.path.exists(dest_dir):
        print(f"Creating directory: {dest_dir}...")
        os.makedirs(dest_dir)

    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        copy_files_recursive(source_item, dest_dir)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:]
    raise Exception("No title header found in markdown file")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}/template.html...")
    
    # Read Markdown
    if os.path.exists(from_path) and os.path.isdir(from_path):
        path_to_text = extract_text_from_file(from_path)
    else:
        raise Exception(f"Directory {from_path} to copy doesn't exist")

    # Read template file
    template_file = ""
    if os.path.exists(template_path) and os.path.isdir(template_path):
        file_path = os.path.join(template_path, "template.html")
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                template_file = f.read()
    else:
        raise Exception(f"Template directory {template_path} doesn't exist")
    
    for rel_path, md_text in path_to_text.items():
        title = extract_title(md_text)
        html_nodes = markdown_to_html_node(md_text)
        page_content = template_file.replace("{{ Title }}", title). \
            replace("{{ Content }}", html_nodes.to_html()). \
            replace('href="/', f'href="{basepath}'). \
            replace('src="/', f'src="{basepath}')
        if rel_path.endswith('.md'):
            rel_path = rel_path.replace('.md', '.html')
        output_file = os.path.join(dest_path, rel_path)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(page_content)
    
def extract_text_from_file(dir_path, root_dir=None):
    if root_dir is None:
        root_dir = dir_path
    relpath_to_content = {}
    for item in os.listdir(dir_path):
        file_path = os.path.join(dir_path, item)
        if os.path.isfile(file_path) and file_path.endswith('.md'):
            with open(file_path, 'r') as f:
                text = f.read()
            rel_path = os.path.relpath(file_path, root_dir)
            relpath_to_content[rel_path] = text
        
        if os.path.isdir(file_path):
            relpath_to_content.update(extract_text_from_file(file_path, root_dir))
    
    return relpath_to_content
