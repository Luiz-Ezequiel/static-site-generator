import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, TextNode, text_to_html_node


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


class TestTextToHtmlNode(unittest.TestCase):

    def test_text_to_html_node_plain_text(self):
        text_node = TextNode('Hello', 'text')
        expected = LeafNode(None, 'Hello')
        result = text_to_html_node(text_node)
        self.assertEqual(result, expected)

    def test_text_to_html_node_bold_text(self):
        text_node = TextNode('Bold Text', 'bold')
        expected = LeafNode('b', 'Bold Text')
        result = text_to_html_node(text_node)
        self.assertEqual(result, expected)

    def test_text_to_html_node_italic_text(self):
        text_node = TextNode('Italic Text', 'italic')
        expected = LeafNode('i', 'Italic Text')
        result = text_to_html_node(text_node)
        self.assertEqual(result, expected)

    def test_text_to_html_node_code_text(self):
        text_node = TextNode('print("Hello World")', 'code')
        expected = LeafNode('code', 'print("Hello World")')
        result = text_to_html_node(text_node)
        self.assertEqual(result, expected)

    def test_text_to_html_node_link_text(self):
        text_node = TextNode('Boot.dev', 'link', url='https://boot.dev.com')
        expected = LeafNode('a', 'Boot.dev', {'href': 'https://boot.dev.com'})
        result = text_to_html_node(text_node)
        self.assertEqual(result, expected)

    def test_text_to_html_node_image_text(self):
        text_node = TextNode( 'Logo', 'image', url='https://boot.dev/logo.png')
        expected = LeafNode('img', None, {'src': 'https://boot.dev/logo.png', 'alt': 'Logo'})
        result = text_to_html_node(text_node)
        self.assertEqual(result, expected)

    def test_text_to_html_node_invalid_text_type(self):
        text_node = TextNode('unsupported', 'Text')
        with self.assertRaises(Exception) as context:
            text_to_html_node(text_node)
        self.assertEqual(str(context.exception), "Text type not valid")


if __name__ == "__main__":
    unittest.main()
