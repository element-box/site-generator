import unittest

from blocktypes import BlockType, block_to_block_type
from utils import markdown_to_blocks, markdown_to_html_node, extract_title
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    ''' HTMLNode'''
    def test_parent_to_html(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

    def test_html_values(self):
        node = HTMLNode('div', 'This is a value string')

        self.assertEqual(node.tag, 'div')
        self.assertEqual(node.value, 'This is a value string')
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props_to_html(self):
        prop_dict = {"href": "https://boot.dev", "target": "_blank"}
        node = HTMLNode(props=prop_dict)
        test_output = node.props_to_html()
        valid_prop = ' href="https://boot.dev" target="_blank"'
        self.assertEqual(test_output, valid_prop)
    
    def test_html_repr(self):
        prop_dict = {"href": "https://boot.dev", "target": "_blank"}
        node = HTMLNode(props=prop_dict)
        self.assertEqual(node.__repr__(), "HTMLNode(None, None, None, {'href': 'https://boot.dev', 'target': '_blank'})")

    ''' LeafNode '''
    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_tag(self):
        self.assertEqual(LeafNode(None, "Value populated!").to_html(), "Value populated!")

    def test_leaf_node_none_value(self):
        with self.assertRaises(ValueError):
            LeafNode(None, None).to_html()
    
    def test_leaf_repr(self):
        prop_dict = {"href": "https://boot.dev", "target": "_blank"}
        node = HTMLNode(props=prop_dict)
        self.assertEqual(node.__repr__(), "HTMLNode(None, None, None, {'href': 'https://boot.dev', 'target': '_blank'})")

    def test_text_type_to_leaf(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        bold_node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(bold_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

        italic_node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(italic_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

        code_node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(code_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

        link_node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev/u/element_box")
        html_node = text_node_to_html_node(link_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props['href'], "https://www.boot.dev/u/element_box")

        image_node = TextNode("This is an image node", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp")
        html_node = text_node_to_html_node(image_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props['src'], "https://www.boot.dev/img/bootdev-logo-full-small.webp")
        self.assertEqual(html_node.props['alt'], "This is an image node")

    def test_text_type_to_wrong_type(self):
        with self.assertRaises(Exception, msg="invalid text type"):
            node = TextNode("This is a text node", TextType.BOLDTEXT)

    ''' ParentNode '''
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_headers(self):
        md = """
# This is a header

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

## This is a smaller header

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a header",
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "## This is a smaller header",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_types_headers(self):
        header_single = "# This is a header"
        self.assertEqual(BlockType.HEADING, block_to_block_type(header_single))

        header_double = "## This is a header"
        self.assertEqual(BlockType.HEADING, block_to_block_type(header_double))

        header_triple = "### This is a header"
        self.assertEqual(BlockType.HEADING, block_to_block_type(header_triple))

        header_quad = "#### This is a header"
        self.assertEqual(BlockType.HEADING, block_to_block_type(header_quad))

        header_quint = "##### This is a header"
        self.assertEqual(BlockType.HEADING, block_to_block_type(header_quint))

        header_sext = "###### This is a header"
        self.assertEqual(BlockType.HEADING, block_to_block_type(header_sext))

        header_sept = "####### This is NOT header"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(header_sept))

    def test_block_to_block_types_code(self):
        code_block = "```this is a code block in markdown```"
        self.assertEqual(BlockType.CODE, block_to_block_type(code_block))

        not_code_block = "``` this is not a valid block"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(not_code_block))

        also_not_code_block = "this is not a valid block```"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(also_not_code_block)) 


    def test_block_to_block_types_quote(self):
        quote_block = "> this is a simple quote block"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(quote_block))

        quote_block_also = ">this is also a quote block"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(quote_block_also))

        not_quote = " > this is not a quote because of the space"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(not_quote))
    
        not_quote_also = " this is not a > quote because the indicator is not at the beginning of the line"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(not_quote_also))


    def test_block_to_block_types_unordered(self):
        single_item = "- This is a list"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(single_item))

        double_items = "- This is a list\n- with items"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(double_items))

        multiple_items = "- This is a list\n- with items\n- and multiples\n- for edge cases\n- and thoroughness"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(multiple_items))

        not_unordered_list = " - This is a list - with items"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(not_unordered_list))

    def test_block_to_block_types_ordered(self):
        single_item = "1. This is a list"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(single_item))

        double_items = "1. This is a list\n2. with items"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(double_items))

        multiple_items = "1. This is a list\n2. with items\n3. and multiples\n4. for edge cases\n5. and thoroughness"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(multiple_items))

        not_ordered_list = "1. This is a list\n3. with items\n2. out of order"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(not_ordered_list))

    def test_headers(self):
        md = """
# This is header 1

## This is header 2

### This is header 3

#### This is header 4

##### This is header 5

###### This is header 6

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is header 1</h1><h2>This is header 2</h2><h3>This is header 3</h3><h4>This is header 4</h4><h5>This is header 5</h5><h6>This is header 6</h6></div>",
        )

    def test_blockquote(self):
        md = """
> This is a block quote

>This is also a blockquote
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a block quote</blockquote><blockquote>This is also a blockquote</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- This is a list
- doesn't matter
- where the order
- but still
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>doesn't matter</li><li>where the order</li><li>but still</li></ul></div>",
        )

    def test_unordered_list(self):
        md = """
1. This is a list
2. where the order
3. does matter
4. actually
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is a list</li><li>where the order</li><li>does matter</li><li>actually</li></ol></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title(self):
        md = """
# Title Header is Valid!
"""
        extracted_title = extract_title(md)
        self.assertEqual(
            extracted_title,
            "Title Header is Valid!"
        )

        md = """
## Header 2 with bad formatting, but still valid

# Title Header is out of order, but ok!
"""
        extracted_title = extract_title(md)
        self.assertEqual(
            extracted_title,
            "Title Header is out of order, but ok!"
        )


    def test_negative_extract_title(self):
        with self.assertRaises(Exception, msg="No title header found in markdown file"):
            extract_title("This is just a standard paragraph.")
        
        with self.assertRaises(Exception, msg="No title header found in markdown file"):
            extract_title("## This is header 2 but not 1")


if __name__ == "__main__":
    unittest.main()