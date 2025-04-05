def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    final_blocks = []
    for block in blocks:
        block = block.strip()
        if block != "":
            final_blocks.append(block)
    return final_blocks