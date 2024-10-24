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

        new_nodes.extend(process_text(node.text, delimiter, text_type))

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

def process_text(text, delimiter, text_type):
    if not delimiter:
        return [TextNode(text, TextType.TEXT)]

    first = text.find(delimiter)
    if first == -1:
        return [TextNode(text, TextType.TEXT)]

    second = text.find(delimiter, first + 1)
    if second == -1:
        raise ValueError("Closing delimiter not found")

    before = text[0:first]
    during = text[first + 1:second]
    after = text[second + 1:]

    result = []

    if before:
        result.append(TextNode(before, TextType.TEXT))

    result.append(TextNode(during, text_type))

    if after:
        result.extend(process_text(after, delimiter, text_type))

    return result

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
