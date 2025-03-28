import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html_1(self):
        node = HTMLNode("p", "this is a paragraph", props={"href": "https://www.google.com", "target": "_blank",})
        html = " href='https://www.google.com' target='_blank'"
        self.assertEqual(node.props_to_html(), html)
    
    def test_props_to_html_2(self):
        node = HTMLNode("p", "this is a paragraph", props={"href": "https://boot.dev", "target": "_hello",})
        html = " href='https://boot.dev' target='_hello'"
        self.assertEqual(node.props_to_html(), html)

    def test_repr(self):
        node = HTMLNode("p", "this is a paragraph")
        repr = "HTMLNode(p, this is a paragraph, None, None)"
        self.assertEqual(node.__repr__(), repr)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href='https://www.google.com'>Click me!</a>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_children_props(self):
        child_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><a href='https://www.google.com'>Click me!</a></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_with_mult_children(self):
        child_node1 = LeafNode("span", "child")
        child_node2 = LeafNode("p", "children")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><p>children</p></div>")

    def test_to_html_with_no_chilren(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_no_tag(self):
        node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            node.to_html()
    


if __name__ == "__main__":
    unittest.main()