import unittest

from textnode import TextNode, TextType
from test_htmlnode import LeafNode


def main():
    text_node = TextNode('This is anchor text', TextType.NORMAL, 'https://www.boot.dev')
    print(text_node)



if __name__ == "__main__":
    main()