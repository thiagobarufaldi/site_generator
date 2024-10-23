import unittest

from node_operations import *
from text_node import TextNode, TextType
from leaf_node import LeafNode

class TestNodeConverters(unittest.TestCase):
    def test_txt(self):
        node = text_node_to_html_node(TextNode("All truly strong people are kind", TextType.TEXT))
        expected_output = LeafNode(None, "All truly strong people are kind")
        self.assertEqual(node, expected_output)

    def test_bold(self):
        node = text_node_to_html_node(TextNode("Do you see how infinite you are?", TextType.BOLD))
        expected_output = LeafNode("b", "Do you see how infinite you are?")
        self.assertEqual(node, expected_output)

    def test_italic(self):
        node = text_node_to_html_node(TextNode("Seek nothing outside of yourself", TextType.ITALIC))
        expected_output = LeafNode("i", "Seek nothing outside of yourself")
        self.assertEqual(node, expected_output)

    def test_code(self):
        node = text_node_to_html_node(TextNode("Think lightly of yourself and deeply of the world", 
                                               TextType.CODE))
        expected_output = LeafNode("code", "Think lightly of yourself and deeply of the world")
        self.assertEqual(node, expected_output)

    def test_link(self):
        node = text_node_to_html_node(TextNode("Takehiko Inoue Website", TextType.LINK, 
                                               "https://itplanning.co.jp/en/"))
        expected_output = LeafNode("a", "Takehiko Inoue Website",
                                   {"href": "https://itplanning.co.jp/en/"})
        self.assertEqual(node, expected_output)

    def test_image(self):
        node = text_node_to_html_node(TextNode("Nice France", TextType.IMAGE, 
                                               "https://example.com/image.jpg"))
        expected_output = LeafNode("img", "",
                                   {"src": "https://example.com/image.jpg", "alt": "Nice France"})
        self.assertEqual(node, expected_output)

    def test_empty(self):
        node = text_node_to_html_node(TextNode("", TextType.TEXT))
        expected_output = LeafNode(None, "")
        self.assertEqual(node, expected_output)

    def test_does_not_exist(self):
        with self.assertRaises(Exception):
            text_node_to_html_node(TextNode("I don't exist", "INVALID_TYPE"))

class TestNodeSplit(unittest.TestCase):
    def test_split_text(self):
        node = TextNode("This is a text with a `code block` word", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_output = [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(nodes, expected_output)

    def test_split_no_delimiter(self):
        node = TextNode("This is a text with no delimiters", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "", TextType.TEXT)
        expected_output = [TextNode("This is a text with no delimiters", TextType.TEXT)]
        self.assertEqual(nodes, expected_output)

    def test_split_invalid_delimiter(self):
        node = TextNode("This is a text with *invalid syntax", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.ITALIC)

    def test_split_multiple_delimiters(self):
        node = TextNode("This is a text with `two` `code blocks`", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_output = [
            TextNode("This is a text with ", TextType.TEXT), 
            TextNode("two", TextType.CODE),
            TextNode(" ", TextType.TEXT), 
            TextNode("code blocks", TextType.CODE)
        ]
        self.assertEqual(nodes, expected_output)

class TestExtractLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

if __name__ == "__main__":
    unittest.main()
