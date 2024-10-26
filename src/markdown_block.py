def markdown_to_blocks(markdown: str):
    if len(markdown) > 0:
        blocks = markdown.split('\n\n')
        return blocks
