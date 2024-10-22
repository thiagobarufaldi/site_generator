from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children):
        super().__init__(tag, None, children)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")

        if not self.children:
            raise ValueError("ParentNode must have at least one child")

        child_html = []
        for child in self.children:
            try:
                child_html.append(child.to_html())
            except ValueError:
                continue

        return f"<{self.tag}>{''.join(child_html)}</{self.tag}>"
