import unittest

from html_node import HTMLNode
from leaf_node import LeafNode
from parent_node import ParentNode

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
        expected_repr = ("<tag=h1, val='best game', child=[], props={'href': 'https://half-life.com'}>")
        self.assertEqual(repr(node), expected_repr)

    def test_repr_empty(self):
        node = HTMLNode(tag="p", value="The cake is a lie")
        expected_repr = "<tag=p, val='The cake is a lie', child=[], props={}>"
        self.assertEqual(repr(node), expected_repr)

class TestLeafNode(unittest.TestCase):
    def test_leaf_complete(self):
        node = LeafNode(tag="p", value="May We Never Need You Again")
        expected_output = "<p>May We Never Need You Again</p>"
        self.assertEqual(node.to_html(), expected_output)

    def test_leaf_tag_empty(self):
        node = LeafNode(tag=None, value="May We Never Need You Again")
        expected_output = "May We Never Need You Again"
        self.assertEqual(node.to_html(), expected_output)

    def test_leaf_value_empty(self):
        node = LeafNode(tag="a", value=None)
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_parent_node_creation(self):
        node = ParentNode("div", [LeafNode("p", "I have a bad feeling about this")])
        self.assertIsInstance(node, ParentNode)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)

    def test_to_html_simple(self):
        node = ParentNode("h1", [LeafNode("p", "I have a bad feeling about this")])
        expected_html = "<h1><p>I have a bad feeling about this</p></h1>"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_multiple_children(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold"),
            LeafNode(None, "Normal"),
            LeafNode("i", "Italic")
        ])
        expected_html = "<p><b>Bold</b>Normal<i>Italic</i></p>"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_nested(self):
        node = ParentNode("div", [
            ParentNode("p", [
                LeafNode("b", "Bold"),
                LeafNode(None, "Normal"),
                LeafNode("i", "Italic")
            ]),
            LeafNode("br", None)
        ])
        expected_html = "<div><p><b>Bold</b>Normal<i>Italic</i></p><br /></div>"
        self.assertEqual(node.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()
