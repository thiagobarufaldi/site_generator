import unittest

from markdown_block import block_to_block_type, markdown_to_blocks

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

    def test_markdown_paragraph(self):
        test_input = "Hey Freeman, good to see you"
        result = block_to_block_type(test_input)
        expected_output = "paragraph"
        self.assertEqual(result, expected_output)

if __name__ == "__main__":
    unittest.main()
