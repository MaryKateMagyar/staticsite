import unittest

from htmlnode import *


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

    def test_paragraphs(self):
        md = """This is **bolded** paragraph
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
```This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_list(self):
        md = """
- Item 1
- Item 2
- Item 3 with **bold** text
"""
    
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3 with <b>bold</b> text</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item with _italic_
3. Third item with `code`
"""
    
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <i>italic</i></li><li>Third item with <code>code</code></li></ol></div>"
        )

    def test_mixed_markdown_elements(self):
        md = """
# Main Heading

## Secondary Heading

This is a paragraph with **bold** and _italic_ and `code` elements.

> This is a blockquote with **formatting** inside it.

### Lists Below

- Unordered item 1
- Unordered item 2 with *emphasis*

1. Ordered item 1
2. Ordered item 2 with `code`

```
def example_function():
# This code block should not process markdown
print("Hello **world**")
```
"""
    
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Main Heading</h1><h2>Secondary Heading</h2><p>This is a paragraph with <b>bold</b> and <i>italic</i> and <code>code</code> elements.</p><blockquote>This is a blockquote with <b>formatting</b> inside it.</blockquote><h3>Lists Below</h3><ul><li>Unordered item 1</li><li>Unordered item 2 with <i>emphasis</i></li></ul><ol><li>Ordered item 1</li><li>Ordered item 2 with <code>code</code></li></ol><pre><code>def example_function():\n# This code block should not process markdown\nprint(\"Hello **world**\")\n</code></pre></div>"
        )
    


if __name__ == "__main__":
    unittest.main()