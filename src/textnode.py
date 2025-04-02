from enum import Enum

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

