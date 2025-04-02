import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    split_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
        elif delimiter not in node.text:
            split_nodes.append(node)
        elif node.text.count(delimiter) % 2 != 0:
            raise Exception("invalid Markdown syntax: missing closing delimiter")
        else:
            new_nodes = []
            split_text = node.text.split(delimiter)
            for index, text in enumerate(split_text):
                if text == "":
                    continue
                elif index % 2 == 0:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                elif index % 2 == 1:
                    new_nodes.append(TextNode(text, text_type))
            split_nodes.extend(new_nodes)
    return split_nodes



def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)