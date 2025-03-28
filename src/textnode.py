from enum import Enum
from htmlnode import *

class TextType(Enum):
    TEXT = "normal text"  # plain text
    BOLD = "bold text"      # **Bold text**
    ITALIC = "italic text"  # _Italic text_
    CODE = "code text"      # `Code text`
    LINK = "link"           # [anchor text](url)
    IMAGE = "image"         # ![alt text](url)

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text  # The text content of the node
        self.text_type = text_type  # The type of text this node contains, which is a member of the TextType enum
        self.url = url  # The URL of the link or image, if the text is a link

    def __eq__(self, target):
        if self.text == target.text and self.text_type == target.text_type and self.url == target.url:
            return True
    
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
        case _:
            raise Exception("text_node is not a valid text type")