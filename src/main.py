import unittest

from textnode import TextNode, TextType
from utils import copy_dir_to_dest, generate_page


def main():
    text_node = TextNode('This is anchor text', TextType.TEXT, 'https://www.boot.dev')
    print(text_node)

    copy_dir_to_dest('static', 'public')

    generate_page('content', '.', 'public')


if __name__ == "__main__":
    main()