from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

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
        case __:
            raise Exception("invalid text node type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            split = old_node.text.split(delimiter)
            if len(split) % 2 == 0:
                raise Exception("invalid markdown syntax, no closing deliminator found")
            for i in range(len(split)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(split[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            if old_node.text != "":
                new_nodes.append(old_node)
        else:
            if old_node.text == "":
                continue

            images = extract_markdown_images(old_node.text)
            if images == []:
                new_nodes.append(old_node)
            else:
                text = old_node.text
                for image_alt, image_link in images:
                    sections = text.split(f"![{image_alt}]({image_link})", 1)
                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                    if len(sections) == 2:
                        text = sections[1]
                    else:
                        text = ""
                if text != "":
                    new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            if old_node.text != "":
                new_nodes.append(old_node)
        else:
            if old_node.text == "":
                continue

            links = extract_markdown_links(old_node.text)
            if links == []:
                new_nodes.append(old_node)
            else:
                text = old_node.text
                for anchor_text, link_url in links:
                    sections = text.split(f"[{anchor_text}]({link_url})", 1)
                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(anchor_text, TextType.LINK, link_url))
                    if len(sections) == 2:
                        text = sections[1]
                    else:
                        text = ""
                if text != "":
                    new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes
