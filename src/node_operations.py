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
    image_url = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return image_url

def extract_markdown_links(text):
    link_url = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link_url

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_nodes = []
        images = extract_markdown_images(node.text)

        remaining_text = node.text
        if images:
            for img_alt, img_url in images:
                markdown = f"![{img_alt}]({img_url})"
                sections = remaining_text.split(markdown, 1)

                if sections[0] != "":
                    split_nodes.append(TextNode(sections[0], TextType.TEXT))
                split_nodes.append(TextNode(img_alt, TextType.IMAGE, img_url))
                if sections[-1] != "":
                    remaining_text = sections[-1]
            if remaining_text != "":
                split_nodes.append(TextNode(remaining_text, TextType.TEXT))
        else:
            new_nodes.append(node)

        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_nodes = []
        links = extract_markdown_links(node.text)

        remaining_text = node.text
        if links:
            for link_alt, link_url in links:
                markdown = f"[{link_alt}]({link_url})"
                sections = remaining_text.split(markdown, 1)

                if sections[0] != "":
                    split_nodes.append(TextNode(sections[0], TextType.TEXT))
                split_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
                if sections[-1] != "":
                    remaining_text = sections[-1]
            if remaining_text != "":
                split_nodes.append(TextNode(remaining_text, TextType.TEXT))
        else:
            new_nodes.append(node)

        new_nodes.extend(split_nodes)
    return new_nodes
