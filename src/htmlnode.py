class HTMLNode():
    def __init__(self, tag=None, value=None, children=[], props={}):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        props_list = []
        for key,value in self.props.items():
            props_list.append(f' {key}="{value}"')
        return ''.join(props_list)

    def __repr__(self):
        return f"<tag={self.tag}, val='{self.value}', child={self.children}, props={self.props}>"
