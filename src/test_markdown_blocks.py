import unittest

from markdown_block import markdown_to_blocks

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

if __name__ == "__main__":
    unittest.main()
