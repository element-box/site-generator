import unittest
import sys

from textnode import TextNode, TextType
from utils import copy_dir_to_dest, generate_page

dir_path_static = "static"
dir_path_public = "docs"
dir_path_content = "content"
template_path = "."

def main():

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = '/'
    text_node = TextNode('This is anchor text', TextType.TEXT, 'https://www.boot.dev')

    copy_dir_to_dest(dir_path_static, dir_path_public)

    generate_page(dir_path_content, template_path, dir_path_public, basepath)


if __name__ == "__main__":
    main()