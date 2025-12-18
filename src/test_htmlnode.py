import unittest

from htmlnode import HTMLNode, LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq_repr(self):
        node = HTMLNode("p", "This is a HTML node")
        text = "HTMLNode(p, This is a HTML node, None, None)"
        self.assertEqual(f"{node}", text)

    def test_eq_prop_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank",})
        html_output = node.props_to_html()
        output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(html_output, output)

    def test_eq_no_props_to_html(self):
        node = HTMLNode()
        html_output = node.props_to_html()
        output = ""
        self.assertEqual(html_output, output)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_raw(self):
        node = LeafNode(None, "this is RAW")
        self.assertEqual(node.to_html(), "this is RAW")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_no_value2(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()