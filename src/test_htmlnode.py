import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()