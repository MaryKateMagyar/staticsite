import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
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

    def test_header_one(self):
        block = "# This is a header"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_header_two(self):
        block = "## This is a header"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_header_three(self):
        block = "### This is a header"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_header_four(self):
        block = "#### This is a header"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_header_five(self):
        block = "##### This is a header"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_header_six(self):
        block = "###### This is a header"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_header_too_many(self):
        block = "######### This is a header"
        self.assertNotEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code(self):
        block = "```\nThis is a block of code\nwith two lines```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_fail(self):
        block = "```This block does not start with a new line```"
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_fail_two(self):
        block = "``\nThis block is missing a back tick```"
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_fail_three(self):
        block = "```\nThis block is missing a closing tick``"
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> This is a quote\n> quote quote quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote(self):
        block = ">This not is a quote\n>quote quote quote"
        self.assertNotEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- This is a list \n- with no order"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_fail(self):
        block = "- This list \n-is missing a space"
        self.assertNotEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. This is a list\n2. with a set order\n3. that increases by one\n4. with each line"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_fail_one(self):
        block = "2. This list does not \n3. start with 1"
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_fail_two(self):
        block = "1. This list \n2.is missing a space \n3. so it fails"
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_fail_three(self):
        block = "1. This list \n5. does not increase by one \n6. so it fails"
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = "This is just a normal paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

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
    
    # def test_simple_title(self):
    #     markdown = "# Simple Title"
    #     self.assertEqual(extract_title(markdown), "Simple Title")
    
    # def test_title_with_whitespace(self):
    #     markdown = "#    Title with spaces    "
    #     self.assertEqual(extract_title(markdown), "Title with spaces")
    
    # def test_multiline_with_title(self):
    #     markdown = "Some text\n# The Title\nMore text"
    #     self.assertEqual(extract_title(markdown), "The Title")
    
    # def test_no_title(self):
    #     markdown = "No title in this text"
    #     with self.assertRaises(Exception):
    #         extract_title(markdown)
    
    # def test_wrong_header_level(self):
    #     markdown = "## This is h2, not h1"
    #     with self.assertRaises(Exception):
    #         extract_title(markdown)