from htmlnode import HTMLNode
from constants import VOID_ELEMENTS

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        if props is None:
            props = {}
        super().__init__(tag, value, None, props)
        self.value = value

    def to_html(self):
        if self.tag in VOID_ELEMENTS:
            return f"<{self.tag} />"
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
