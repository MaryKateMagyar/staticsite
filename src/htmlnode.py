class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""

        html_output = ""

        for key, value in self.props.items():
            html_output += f' {key}="{value}"'

        return html_output

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")
        if not self.tag:
            return self.value
        output = f"<{self.tag}"
        if self.props:
            output += self.props_to_html()
        output += f">{self.value}</{self.tag}>"
        return output 

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("all parent nodes must have a tag")
        if not self.children:
            raise ValueError("all parent nodes must have children")
        output = f"<{self.tag}"
        if self.props:
            output += self.props_to_html()
        output += ">"
        for child in self.children:
            output += child.to_html()
        output += f"</{self.tag}>"
        return output
        

        
        