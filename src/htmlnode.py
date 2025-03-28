class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag            # A string representing the HTML tag name (e.g. "p", "a", "h1", etc. )
        self.value = value        # A string representing the valye of the HTML tag (e.g. the text inside a paragraph)
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
        


        