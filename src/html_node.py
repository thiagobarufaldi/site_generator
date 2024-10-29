class HTMLNode():
    def __init__(self, tag=None, value=None, children=[], props={}):
        self.tag = tag
        self.value = value.strip() if value else value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        props_list = []
        for key,value in self.props.items():
            props_list.append(f' {key}="{value}"')
        return ''.join(props_list)

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )

    def __repr__(self):
        return f"<tag={self.tag}, val='{self.value}', children={self.children}, props={self.props}>"
