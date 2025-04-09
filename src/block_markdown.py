import re
from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block.lstrip("# ").strip()
    raise Exception("missing h1 header")

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    final_blocks = []
    for block in blocks:
        block = block.strip()
        if block != "":
            final_blocks.append(block)
    return final_blocks

def check_if_quote_block(block):
    split_lines = block.splitlines()
    for line in split_lines:
        if not line.startswith(">"):
            return False
    return True

def check_if_unordered_list(block):
    split_lines = block.splitlines()
    for line in split_lines:
        if not line.startswith("- "):
            return False
    return True

def check_if_ordered_list(block):
    split_lines = block.splitlines()
    count = 1
    for line in split_lines:
        if not line.startswith(f"{count}. "):
            return False
        count += 1
    return True

def block_to_block_type(block):
    if re.match(r"#{1,6} \S", block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif check_if_quote_block(block):
        return BlockType.QUOTE
    elif check_if_unordered_list(block):
        return BlockType.UNORDERED_LIST
    elif check_if_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_block(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ul_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ol_to_html_node(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def heading_to_html_node(block):
    tier = 0
    for char in block:
        if char == "#":
            tier += 1
        else:
            break
    if tier + 1 >= len(block):
        raise ValueError(f"invalid heading: h{tier}")
    text = block[tier + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{tier}", children)

def code_to_html_block(block):
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    children = text_node_to_html_node(raw_text_node)
    code_node = ParentNode("code", [children])
    return ParentNode("pre", [code_node])

def quote_to_html_node(block):
    lines = block.splitlines()
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(">").strip())
    text = " ".join(new_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def ul_to_html_node(block):
    lines = block.splitlines()
    new_lines = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        new_lines.append(ParentNode("li", children))
    return ParentNode("ul", new_lines)

def ol_to_html_node(block):
    lines = block.splitlines()
    new_lines = []
    for line in lines:
        text = line[3:]
        children = text_to_children(text)
        new_lines.append(ParentNode("li", children))
    return ParentNode("ol", new_lines)

def paragraph_to_html_node(block):
    lines = block.splitlines()
    text = " ".join(lines)
    children = text_to_children(text)
    return ParentNode("p", children)