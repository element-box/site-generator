import unittest

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
        print(node.to_html())
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

if __name__ == "__main__":
    unittest.main()