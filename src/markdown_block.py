from constants import BLOCK_TYPES
from html_node import HTMLNode
from parent_node import ParentNode

def markdown_to_blocks(markdown: str):
    if not markdown:
        return []

    blocks = markdown.split('\n\n')
    clean_blocks = [block.strip() for block in blocks]
    complete_blocks = list(filter(None, clean_blocks))

    return complete_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BLOCK_TYPES["block_type_heading"]

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BLOCK_TYPES["block_type_code"]

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BLOCK_TYPES["block_type_paragraph"]
        return BLOCK_TYPES["block_type_quote"]

    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return BLOCK_TYPES["block_type_paragraph"]
        return BLOCK_TYPES["block_type_ulist"]

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BLOCK_TYPES["block_type_paragraph"]
        return BLOCK_TYPES["block_type_ulist"]

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BLOCK_TYPES["block_type_paragraph"]
            i += 1
        return BLOCK_TYPES["block_type_olist"]
    return BLOCK_TYPES["block_type_paragraph"]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html = create_block_node(block, block_type)
        html_nodes.append(html)

    return HTMLNode("div", children=html_nodes)

def create_block_node(block, type):
    match type:
        case "heading":
            level = get_heading_level(block)
            content = block.lstrip("#").strip()
            return HTMLNode(tag=level, value=content)

        case "code":
            content = block.strip("```")
            return HTMLNode(ParentNode("pre")

def get_heading_level(block):
    stripped_heading = block.lstrip()
    i = 0
    for head in stripped_heading:
        if head != '#':
            break
        i += 1

    return f"h{i}"
