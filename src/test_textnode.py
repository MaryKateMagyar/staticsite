import unittest

from textnode import *
from splitnodes import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.LINK, "www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "www.boot.dev")
        self.assertEqual(node, node2)

    def test_type_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is random text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boots.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://www.boots.dev"})

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.boots.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.boots.dev", "alt": "This is a text node"})

    def test_split_nodes_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_results = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes, expected_results)

    def test_split_nodes_not_TEXT(self):
        node = TextNode("This is text with a code block", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_results = [TextNode("This is text with a code block", TextType.CODE)]
        self.assertEqual(new_nodes, expected_results)

    def test_split_nodes_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_results = [TextNode("This is text with a ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes, expected_results)

    def test_split_nodes_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_results = [TextNode("This is text with a ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes, expected_results)

    def test_split_nodes_multiple_nodes1(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is another text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        expected_results = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT), TextNode("This is another text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes, expected_results)

    def test_split_nodes_multiple_nodes2(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is another text but with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        expected_results = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT), TextNode("This is another text but with a **bold** word", TextType.TEXT)]
        self.assertEqual(new_nodes, expected_results)

    def test_split_nodes_multiple_nodes3(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is another text but with a bold line", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        expected_results = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT), TextNode("This is another text but with a bold line", TextType.BOLD)]
        self.assertEqual(new_nodes, expected_results)

    def test_split_nodes_multiple_nodes4(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is another text but with a bold line", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        expected_results = [TextNode("This is text with a `code block` word", TextType.TEXT), TextNode("This is another text but with a bold line", TextType.BOLD)]
        self.assertEqual(new_nodes, expected_results)


if __name__ == "__main__":
    unittest.main()