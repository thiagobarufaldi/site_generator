import re
from constants import BLOCK_TYPES
from html_node import HTMLNode

def markdown_to_blocks(markdown: str):
    if not markdown:
        return []

    blocks = markdown.split('\n\n')
    clean_blocks = [block.strip() for block in blocks]
    complete_blocks = list(filter(None, clean_blocks))

    return complete_blocks

def block_to_block_type(block):
    lines = block.split('\n')
    clean_lines = get_cleaned_list_items(block)

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BLOCK_TYPES["block_type_heading"]

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BLOCK_TYPES["block_type_code"]

    if block.startswith(">"):
        for line in clean_lines:
            if not line.startswith(">"):
                return BLOCK_TYPES["block_type_paragraph"]
        return BLOCK_TYPES["block_type_quote"]

    if block.startswith("* "):
        for line in clean_lines:
            if not line.startswith("* "):
                return BLOCK_TYPES["block_type_paragraph"]
        return BLOCK_TYPES["block_type_ulist"]

    if block.startswith("- "):
        for line in clean_lines:
            if not line.startswith("- "):
                return BLOCK_TYPES["block_type_paragraph"]
        return BLOCK_TYPES["block_type_ulist"]

    if re.match(r'^\d+\.\s', lines[0]):
        for line in clean_lines:
            if not re.match(r'^\d+\.\s', line):
                return BLOCK_TYPES["block_type_paragraph"]
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
            code_node = HTMLNode("code", value=content)
            return HTMLNode("pre", children=[code_node])

        case "quote":
            content = block.strip(">")
            return HTMLNode("blockquote", value=content)

        case "ordered_list":
            list_items = get_cleaned_list_items(block)
            li_nodes = []
            for item in list_items:
                content = re.sub(r'^\d+\.\s', '', item)
                li_nodes.append(HTMLNode("li", value=content))
            return HTMLNode("ol", children=li_nodes)

        case "unordered_list":
            list_items = get_cleaned_list_items(block)
            li_nodes = []
            for item in list_items:
                if item.startswith("* "):
                    content = item.strip("* ")
                    li_nodes.append(HTMLNode("li", value=content))
                elif item.startswith("- "):
                    content = item.strip("- ")
                    li_nodes.append(HTMLNode("li", value=content))
            return HTMLNode("ul", children=li_nodes)

        case "paragraph":
            content = block.strip()
            return HTMLNode("p", value=content)


def get_heading_level(block):
    stripped_heading = block.lstrip()
    i = 0
    for head in stripped_heading:
        if head != '#':
            break
        i += 1

    return f"h{i}"

def get_cleaned_list_items(items):
    list_items = items.split('\n')
    clean_items = [item.strip() for item in list_items]
    return clean_items
