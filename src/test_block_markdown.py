import unittest
from block_markdown import BlockType, markdown_to_blocks, block_to_blocktype


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_blocktype(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        type_list = []
        for block in blocks:
            type_list.append(block_to_blocktype(block))
        self.assertEqual(
            type_list,
            [
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.UNORDERED_LIST,
            ],
        )


if __name__ == "__main__":
    unittest.main()
