from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, children, tag, props={}):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Attribute tag must be specified")
        if len(self.children) == 0:
            raise ValueError("ParentNode must have at least one child")

        child_html = []
        for child in self.children:
            child_html.append(child.to_html())

        return f"<{self.tag}>{' '.join(child_html)}</{self.tag}>"
