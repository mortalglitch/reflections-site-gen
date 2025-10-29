from enum import Enum

from htmlnode import ParentNode, LeafNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_blocktype(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    # Goal return a single parentnode that contains many sub nodes and should be wrapped in a div
    current_children = []
    result_parent = ParentNode("div", current_children)
    # split to block
    current_blocks = markdown_to_blocks(markdown)
    # loop each block
    for block in current_blocks:
        # get type of block
        block_type = block_to_blocktype(block)
        # based on type create new htmlnode
        match block_type:
            case BlockType.PARAGRAPH:
                children_node_list = block_to_htmlnodes(block)
                html_children = join_htmlnodes(children_node_list)
                current_children.append(LeafNode("p", html_children))
            case BlockType.CODE:
                block = block[4:-3]
                block = f"<code>{block}</code>"
                current_children.append(LeafNode("pre", block))
            case BlockType.HEADING:
                children_node_list = block_to_htmlnodes(block)
                html_children = join_htmlnodes(children_node_list)
                split_header = html_children.split(" ", 1)
                heading_count = len(split_header[0])
                current_children.append(LeafNode(f"h{heading_count}", html_children[1]))
            case BlockType.ULIST:
                children_node_list = block_to_htmlnodes(block)
                html_children = join_listnodes(children_node_list)
                current_children.append(LeafNode("ul", html_children))
            case BlockType.OLIST:
                children_node_list = block_to_htmlnodes(block)
                html_children = join_listnodes(children_node_list)
                current_children.append(LeafNode("ol", html_children))
            case BlockType.QUOTE:
                children_node_list = block_to_htmlnodes(block)
                html_children = join_htmlnodes(children_node_list)
                current_children.append(LeafNode("blockquote", html_children))

    result_parent.children = current_children
    return result_parent

    # assign child htmlnode objects to block
    #


def block_to_htmlnodes(block):
    block = block.replace("\n", "")
    text_node_list = text_to_textnodes(block)
    html_node_list = []
    for node in text_node_list:
        html_node_list.append(text_node_to_html_node(node))
    return html_node_list


def join_htmlnodes(nodes):
    html_joined = ""
    for node in nodes:
        html_joined += node.to_html()
    return html_joined


def join_listnodes(nodes):
    html_joined = ""
    for node in nodes:
        html_joined += f"<li>{node.to_html}</li>"
    return html_joined
