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

def split_nodes_image(old_nodes):
    split_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue
        node_text = node.text
        new_nodes = []
        extracted_images = extract_markdown_images(node.text)
        if extracted_images == []:
            split_nodes.append(node)
            continue
        for image in extracted_images:
            split_text = node_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("invalid image markdown")
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            node_text = split_text[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
        split_nodes.extend(new_nodes)
    return split_nodes

def split_nodes_link(old_nodes):
    split_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue
        node_text = node.text
        new_nodes = []
        extracted_links = extract_markdown_links(node.text)
        if extracted_links == []:
            split_nodes.append(node)
            continue
        for link in extracted_links:
            split_text = node_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("invalid link markdown")
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            node_text = split_text[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
        split_nodes.extend(new_nodes)
    return split_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    return split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(split_nodes_image(split_nodes_link(nodes)), "`", TextType.CODE), "_", TextType.ITALIC), "**", TextType.BOLD)