import re

from typing import List, Tuple
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes: List, delimiter: str, text_type: TextType) -> List:
    delim_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            delim_list.append(node)
            continue
        
        while node.text.find(delimiter) != -1: 
            delim_index_one = node.text.find(delimiter)

            if delim_index_one < len(node.text) - 1:
                delim_index_two = node.text.find(delimiter, delim_index_one + 1)

            if delim_index_two == -1:
                raise Exception("invalid Markdown syntax: no closing delimiter found")
            
            if delim_index_one > 0:
                delim_list.append(TextNode(node.text[:delim_index_one], TextType.TEXT))

            delim_list.append(TextNode(node.text[delim_index_one + len(delimiter) : delim_index_two], text_type))
            
            node.text = node.text[delim_index_two + len(delimiter):]

        if len(node.text) > 0:
            delim_list.append(TextNode(node.text, TextType.TEXT))

    return delim_list

def extract_markdown_images(text: str) -> List[Tuple]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text: str) -> List[Tuple]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

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
    node = [TextNode(text, TextType.TEXT)]
    node = split_nodes_delimiter(node, "**", TextType.BOLD)
    node = split_nodes_delimiter(node, "_", TextType.ITALIC)
    node = split_nodes_delimiter(node, "`", TextType.CODE)
    node = split_nodes_image(node)
    node = split_nodes_link(node)
    return node