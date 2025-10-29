from block_markdown import BlockType, block_to_blocktype, markdown_to_blocks


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        if (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        ):
            return True
        else:
            return False

    def __repr__(self):
        return f"HTMLNode: Tag:{self.tag}, Value:{self.tag} Children:{self.children} Props:{self.props}"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        prop_string = ""
        for i in self.props:
            new_string = f' {i}="{self.props[i]}"'
            prop_string += new_string
        return prop_string


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if self.tag is None:
            return self.value
        if self.props is not None:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError
        if not self.children:
            raise ValueError("missing children")
        else:
            new_html = f"<{self.tag}>"  # may be missing something
            for i in self.children:
                new_html += i.to_html()
            new_html += f"</{self.tag}>"
            return new_html


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
        if block_type == BlockType.PARAGRAPH:
            pass
        # assign child htmlnode objects to block
