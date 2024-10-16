import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        expected_output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_empty(self):
        node = HTMLNode()
        expected_output = ''
        self.assertEqual(node.props_to_html(), expected_output)

    def test_repr_complete(self):
        node = HTMLNode(tag="h1",value="best game",children=[],props={"href": "https://half-life.com"})
        expected_repr = ('<tag=h1>,val="best game",<child=[]>,'
                         '<props="href": "https://www.half-life.com", "target": "_blank"',)
        self.assertEqual(repr(node), expected_repr)

    def test_repr_empty(self):
        node = HTMLNode(tag="p", value="The cake is a lie")
        expected_repr = '<tag=p>,val="The cake is a lie",<child=[]>,<props={}>'
        self.assertEqual(repr(node), expected_repr)

if __name__ == "__main__":
    unittest.main()
