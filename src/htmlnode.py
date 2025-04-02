from blocktype import *
from textnode import *
from splitnodes import *

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag            # A string representing the HTML tag name (e.g. "p", "a", "h1", etc. )
        self.value = value        # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children  # A list of HTMLNode objects representing the children of this node
        self.props = props        # A dictionary of key-value pairs representing the attributes of the HTML tag
                                  #    for example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
           raise Exception("no props available")
        
        html_string = ""
        for key in self.props:
            value = self.props[key]
            html_string = html_string + f" {key}='{value}'"
        return html_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")
        if self.tag is None:
            return f"{self.value}"
        if self.props != None:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None): 
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent nodes cannot have tag be None")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Parent nodes cannot have children be None")

        html = f"<{self.tag}>"
        if self.props != None:
            html += self.props_to_html()

        for child in self.children:
            html += child.to_html()

        html += f"</{self.tag}>"

        return html

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("text_node is not a valid text type")
        
def block_to_tag(block_type, block=None):
    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            return heading_level(block)
        case BlockType.CODE:
            return "pre"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case _:
            raise Exception("block is not a valid block_type")

def heading_level(block):
    if block.startswith("# "):
        return "h1"
    if block.startswith("## "):
        return "h2"
    if block.startswith("### "):
        return "h3"
    if block.startswith("#### "):
        return "h4"
    if block.startswith("##### "):
        return "h5"
    if block.startswith("###### "):
        return "h6"
    raise Exception("Invalid heading block")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)

    children_nodes = []

    for text_node in text_nodes:
        children_nodes.append(text_node_to_html_node(text_node))

    return children_nodes
    
def list_items_to_html(block, block_type):
    new_lines = []

    if block_type is BlockType.UNORDERED_LIST:
        block = block.replace("\n", "")
        lines = block.split("- ")
        for line in lines[1:]:
            children = text_to_children(line)
            processed_line = ""
            for child in children:
                processed_line += child.to_html()
            new_lines.append(f"<li>{processed_line}</li>")

    elif block_type is BlockType.ORDERED_LIST:
        lines = block.split("\n")
        line_number = 0
        for line in lines:
            if not line:
                continue

            line_number += 1
            pos = line.find(f"{line_number}. ")
            if pos == -1:
                raise Exception(f"Invalid ordered list numbering: Exepected {line_number}. but found ")
            line = line[pos + 3:]
            children = text_to_children(line)
            processed_line = ""
            for child in children:
                processed_line += child.to_html()
            new_lines.append(f"<li>{processed_line}</li>")

    return "".join(new_lines)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    tag = block_to_tag(block_type, block)

    if block_type is BlockType.PARAGRAPH:
        block = block.replace("\n", " ")

    if block_type is BlockType.UNORDERED_LIST or block_type is BlockType.ORDERED_LIST:
        block = list_items_to_html(block, block_type)

    if block_type is BlockType.HEADING:
        block = block.strip("# ")

    if block_type is BlockType.QUOTE:
        block = block.strip("> ")

    if block_type is BlockType.CODE:
        block = block.strip("```")
        if block.startswith("\n"):
            block = block[1:]
        code_node = TextNode(block, TextType.CODE)
        children = [text_node_to_html_node(code_node)]
    else:
        children = text_to_children(block)

    if children == []:
        children = None

    return ParentNode(tag, children)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    children = []

    for block in blocks:
        children.append(block_to_html_node(block))

    return ParentNode("div", children)

        
        