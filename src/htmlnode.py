'''
tag - A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
value - A string representing the value of the HTML tag (e.g. the text inside a paragraph)
children - A list of HTMLNode objects representing the children of this node
props - A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
'''
from textnode import TextNode


class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props:
            result = ''
            for k, v in self.props.items():
                result += f' {k}="{v}"'
            return result
        return ''

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str = None, value: str = None, props: dict = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def __eq__(self, other: object) -> bool:
        return self.tag == other.tag and self.value == other.value and self.props == other.props


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent Nodes must have a tag")
        if len(self.children) == 0 or self.children is None:
            raise ValueError("Parent Nodes must have children")

        start_tag = f"<{self.tag}{self.props_to_html()}>"
        children_html = "".join(child.to_html() for child in self.children)
        end_tag = f"</{self.tag}>"

        return start_tag + children_html + end_tag

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"


def text_to_html_node(text_node: TextNode) -> LeafNode:
    text_types = ['text', 'bold', 'italic', 'code', 'link', 'image']
    if text_node.text_type not in text_types:
        raise Exception("Text type not valid")

    if text_node.text_type == 'text':
        return LeafNode(None, text_node.text)
    elif text_node.text_type == 'bold':
        return LeafNode('b', text_node.text)
    elif text_node.text_type == 'italic':
        return LeafNode('i', text_node.text)
    elif text_node.text_type == 'code':
        return LeafNode('code', text_node.text)
    elif text_node.text_type == 'link':
        return LeafNode('a', text_node.text, {'href': text_node.url})
    else:
        return LeafNode('img', None, {'src': text_node.url, 'alt': text_node.text})
