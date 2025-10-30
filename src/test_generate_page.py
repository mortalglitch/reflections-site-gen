import unittest

from generate_page import extract_title


class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        md = "# This is a title   "
        title = extract_title(md)
        self.assertEqual("This is a title", title)


if __name__ == "__main__":
    unittest.main()
