def markdown_to_blocks(markdown: str):
    if not markdown:
        return []

    blocks = markdown.split('\n\n')
    clean_blocks = [block.strip() for block in blocks]
    complete_blocks = list(filter(None, clean_blocks))

    return complete_blocks
