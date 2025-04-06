import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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