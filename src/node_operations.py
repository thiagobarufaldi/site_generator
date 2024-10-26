import re
from text_node import TextNode, TextType
from leaf_node import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Type specified does not exist.")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        if delimiter == "**":
            nodes = split_bold(text)
            new_nodes.extend(nodes)

        elif delimiter == "*":
            nodes = split_italic(text)
            new_nodes.extend(nodes)

        elif delimiter == "`": 
            nodes = split_code(text)
            new_nodes.extend(nodes)

        else:
            new_nodes.append(node)
            continue

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        current_text = node.text
        for img_alt, img_url in images:
            markdown = current_text.split(f"![{img_alt}]({img_url})", 1)
            if markdown[0] != "":
                new_nodes.append(TextNode(markdown[0], TextType.TEXT))
            new_nodes.append(TextNode(img_alt, TextType.IMAGE, img_url))
            current_text = markdown[-1]

        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        current_text = node.text
        for link_alt, link_url in links:
            markdown = current_text.split(f"[{link_alt}]({link_url})", 1)
            if markdown[0] != "":
                new_nodes.append(TextNode(markdown[0], TextType.TEXT))
            new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
            current_text = markdown[-1]
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes

def extract_markdown_images(text):
    malformed = re.findall(r"!\[\]|\!\[[^\]]*\]\(\)|\!\[[^\]]*\]\(\s*\)", text)
    if malformed:
        raise ValueError("Invalid image markdown - empty alt text or URL")
    image_url = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return image_url

def extract_markdown_links(text):
    malformed = re.findall(r"\[\]|\[[^\]]*\]\(\)|\[[^\]]*\]\(\s*\)", text)
    if malformed:
        raise ValueError("Invalid link markdown - empty text or URL")
    link_url = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link_url

def split_bold(text):
    while '**' in text:
        start = text.find('**')
        end = text.find('**', start + 2)

        if end == -1: 
            raise ValueError("Invalid Markdown: Closing tag not found")

        before_bold = text[:start]
        bold_text = text[start + 2:end]
        text = text[end + 2:]

        nodes = []
        if before_bold:
            nodes.append(TextNode(before_bold, TextType.TEXT))

        if bold_text:
            nodes.append(TextNode(bold_text, TextType.BOLD))

        if text:
            nodes.extend(split_bold(text))

        return nodes

    return [TextNode(text, TextType.TEXT)]

def split_italic(text):
    while '*' in text:
        start = text.find('*')
        end = text.find('*', start + 1)

        if end == -1: 
            raise ValueError("Invalid Markdown: Closing tag not found")

        before_italic = text[:start]
        italic_text = text[start + 1:end]
        text = text[end + 1:]

        nodes = []
        if before_italic:
            nodes.append(TextNode(before_italic, TextType.TEXT))

        if italic_text:
            nodes.append(TextNode(italic_text, TextType.ITALIC))

        if text:
            nodes.extend(split_italic(text))

        return nodes

    return [TextNode(text, TextType.TEXT)]

def split_code(text):
    while '`' in text:
        start = text.find('`')
        end = text.find('`', start + 1)

        if end == -1: 
             raise ValueError("Invalid Markdown: Closing tag not found")

        before_code = text[:start]
        code_text = text[start + 1:end]
        text = text[end + 1:]

        nodes = []
        if before_code:
            nodes.append(TextNode(before_code, TextType.TEXT))

        if code_text:
            nodes.append(TextNode(code_text, TextType.CODE))

        if text:
            nodes.extend(split_code(text))

        return nodes

    return [TextNode(text, TextType.TEXT)]
