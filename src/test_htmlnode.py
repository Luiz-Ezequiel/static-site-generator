import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()
