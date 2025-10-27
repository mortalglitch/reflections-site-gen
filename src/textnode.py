from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, texttype, url=None):
        self.text = text
        self.texttype = texttype
        self.url = url

    def __eq__(self, other):
        if (self.text == other.text
                and self.texttype == other.texttype
                and self.url == other.url):
            return True
        else:
            return False

    def __repr__(self):
        return f'TextNode({self.text}, {self.texttype.value}, {self.url})'


def text_node_to_html_node(text_node):
    match text_node.texttype:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url, })
        case TextType.IMAGE:
            return LeafNode("img", "", {"alt": text_node.text, "src": text_node.url, })
    raise Exception("TextNode is an invalid type for processing")
