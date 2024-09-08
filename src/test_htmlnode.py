import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_constructor(self):
        node = HTMLNode()
        self.assertEqual("HTMLNode(None, None, None, None)", str(node))

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())

    def test_repr(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual("HTMLNode(None, None, None, {'href': 'https://www.google.com', 'target': '_blank'})", repr(node))


class TestLeafNode(unittest.TestCase):
    def test_to_html_with_all_parameters(self):
        node = LeafNode(tag="p", value="Hello, world!", props={"class": "greeting"})
        expected_html = '<p class="greeting">Hello, world!</p>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_missing_tag(self):
        node = LeafNode(value="Hello, world!")
        expected_html = 'Hello, world!'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_missing_value(self):
        node = LeafNode(tag="p")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_no_properties(self):
        node = LeafNode(tag="p", value="Hello, world!")
        expected_html = '<p>Hello, world!</p>'
        self.assertEqual(node.to_html(), expected_html)

    def test_repr(self):
        node = LeafNode("p", "Hello, world!", {"class": "greeting"})
        self.assertEqual("LeafNode(p, Hello, world!, {'class': 'greeting'})", repr(node))


if __name__ == "__main__":
    unittest.main()
