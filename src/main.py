import unittest

from textnode import TextNode, TextType
from test_htmlnode import LeafNode


def main():
    text_node = TextNode('This is anchor text', TextType.NORMAL, 'https://www.boot.dev')
    print(text_node)

def text_node_to_html_node(text_node) -> LeafNode:
    match(text_node.text_type):
        case (TextType.TEXT):
            return LeafNode(None, text_node.text)
        case (TextType.BOLD):
            return LeafNode("b", text_node.text)
        case (TextType.ITALIC):
            return LeafNode("i", text_node.text)
        case (TextType.CODE):
            return LeafNode("code", text_node.text)
        case (TextType.LINK):
            return LeafNode("a", text_node.text, {'href': text_node.url})
        case (TextType.IMAGE):
            return LeafNode("img", "", {'src': text_node.url, 'alt': text_node.text})
        case _:
            raise Exception("invalid text type")


if __name__ == "__main__":
    main()