import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestLeafNode(unittest.TestCase):
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
        self.assertEqual(node.to_html(), "<p></p>")

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

    def test_to_html_with_no_child(self):
        parent_node = ParentNode("a", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_no_tag(self):
        child_node = LeafNode("div", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
    
    def test_to_html_with_children_and_props(self):
        child_node = LeafNode("div", "child")
        parent_node = ParentNode("a", [child_node], {"href": "https://www.google.com"})
        self.assertEqual(
            parent_node.to_html(),
            '<a href="https://www.google.com"><div>child</div></a>'
        )

if __name__ == "__main__":
    unittest.main()