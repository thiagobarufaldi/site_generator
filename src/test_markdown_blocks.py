import unittest

from html_node import HTMLNode
import html_node
from markdown_block import block_to_block_type, markdown_to_blocks, markdown_to_html_node

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        test_input = """#Heading

                        Paragraph text

                        * List item"""
        result = markdown_to_blocks(test_input)
        expected_output = ["#Heading", "Paragraph text", "* List item"]
        self.assertEqual(result, expected_output)

    def test_markdown_empty(self):
        test_input = ""
        result = markdown_to_blocks(test_input)
        expected_output = []
        self.assertEqual(result, expected_output)

    def test_markdown_spaces(self):
        test_input = """#Heading

                        Paragraph text

                        * List item"""
        result = markdown_to_blocks(test_input)
        expected_output = ["#Heading", "Paragraph text", "* List item"]
        self.assertEqual(result, expected_output)

    def test_markdown_multiple_blanks(self):
        test_input = """#Heading


                        Paragraph text


                        * List item"""
        result = markdown_to_blocks(test_input)
        expected_output = ["#Heading", "Paragraph text", "* List item"]
        self.assertEqual(result, expected_output)

class TestMarkdownBlockTypes(unittest.TestCase):
    def test_markdown_heading(self):
        test_input = "# Heading"
        result = block_to_block_type(test_input)
        expected_output = "heading"
        self.assertEqual(result, expected_output)

    def test_markdown_code(self):
        test_input = "```\ncode block\n```"
        result = block_to_block_type(test_input)
        expected_output = "code"
        self.assertEqual(result, expected_output)

    def test_markdown_quote(self):
        test_input = "> When other people talk, listen completely"
        result = block_to_block_type(test_input)
        expected_output = "quote"
        self.assertEqual(result, expected_output)

    def test_markdown_unordered_list(self):
        test_input = "* Gravity gun"
        result = block_to_block_type(test_input)
        expected_output = "unordered_list"
        self.assertEqual(result, expected_output)

    def test_markdown_ordered_list(self):
        test_input = "1. Crowbar"
        result = block_to_block_type(test_input)
        expected_output = "ordered_list"
        self.assertEqual(result, expected_output)

    def test_markdown_un_multiple(self):
        test_input = """* Gravity gun
                        * Crowbar"""
        result = block_to_block_type(test_input)
        expected_output = "unordered_list"
        self.assertEqual(result, expected_output)

    def test_markdown_ol_multiple(self):
        test_input = """1. Crowbar
                        2. 9mm Pistol"""
        result = block_to_block_type(test_input)
        expected_output = "ordered_list"
        self.assertEqual(result, expected_output)

    def test_markdown_paragraph(self):
        test_input = "Hey Freeman, good to see you"
        result = block_to_block_type(test_input)
        expected_output = "paragraph"
        self.assertEqual(result, expected_output)

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_heading_html(self):
        test_input = "# Heading"
        html_res = markdown_to_html_node(test_input)
        expected_output = HTMLNode("div", children=[HTMLNode("h1", "Heading")])
        self.assertEqual(html_res, expected_output)

    def test_markdown_code_html(self):
        test_input = "```\ncoding thingz\n```"
        html_res = markdown_to_html_node(test_input)
        expected_output = HTMLNode("div", children=[
            HTMLNode("pre", children=[HTMLNode("code", value="coding thingz")])
        ])
        self.assertEqual(html_res, expected_output)

    def test_markdown_quote_html(self):
        test_input = "> Things are only impossible until they are not"
        html_res = markdown_to_html_node(test_input)
        expected_output = HTMLNode("div", children=[
            HTMLNode("blockquote", "Things are only impossible until they are not")
        ])
        self.assertEqual(html_res, expected_output)

    def test_markdown_unordered_list_html(self):
        test_input = "* 9mm Pistol"
        html_res = markdown_to_html_node(test_input)
        expected_output = HTMLNode("div", children=[
            HTMLNode("ul", children=[HTMLNode("li", value="9mm Pistol")])
        ])
        self.assertEqual(html_res, expected_output)

    def test_markdown_un_multiple(self):
        test_input = """* 9mm Pistol
                        * Shotgun"""
        html_res = markdown_to_html_node(test_input)
        expected_output = HTMLNode("div", children=[
            HTMLNode("ul", children=[HTMLNode("li", value="9mm Pistol"),
                                     HTMLNode("li", value="Shotgun")])
        ])
        self.assertEqual(html_res, expected_output)

    def test_markdown_ordered_list_html(self):
        test_input = "1. Powered Combat Vest"
        html_res = markdown_to_html_node(test_input)
        expected_output = HTMLNode("div", children=[
            HTMLNode("ol", children=[HTMLNode("li", value="Powered Combat Vest")])
        ])
        self.assertEqual(html_res, expected_output)

    def test_markdown_ol_multiple(self):
        test_input = """1. Powered Combat Vest
                        2. Glasses"""
        html_res = markdown_to_html_node(test_input)
        expected_output = HTMLNode("div", children=[
            HTMLNode("ol", children=[HTMLNode("li", value="Powered Combat Vest"),
                                     HTMLNode("li", value="Glasses")])
        ])
        self.assertEqual(html_res, expected_output)

    def test_markdown_paragraph_html(self):
        test_input = "WE'RE DOOMED"
        html_res = markdown_to_html_node(test_input)
        expected_output = HTMLNode("div", children=[HTMLNode("p", "WE'RE DOOMED")])
        self.assertEqual(html_res, expected_output)

if __name__ == "__main__":
    unittest.main()
