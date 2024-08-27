import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("Text node for test", "italic")
        self.assertEqual(node.url, None)

    def test_eq_false(self):
        node = TextNode("This is a text node for test", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node for test", "bold", "https://www.boot.dev")
        self.assertEqual("TextNode(This is a text node for test, bold, https://www.boot.dev)", repr(node))

if __name__ == "__main__":
    unittest.main()
