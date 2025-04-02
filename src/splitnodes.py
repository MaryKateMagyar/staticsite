import re
from textnode import TextNode, TextType
from htmlnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            node_list.append(old_node)
            continue

        split_nodes = old_node.text.split(delimiter)

        if len(split_nodes) % 2 == 0:
            raise Exception("Invalid Markdown syntax: missing closing delimiter")

        for i in range(len(split_nodes)):
            if split_nodes[i] == "":
                continue
            
            split_type = text_type if i % 2 == 1 else TextType.TEXT
            node_list.append(TextNode(split_nodes[i], split_type))

    return node_list


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return matches


def split_nodes_image(old_nodes):
    node_list = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            node_list.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)

        if images == []:
            node_list.append(old_node)
            continue

        current_text = old_node.text

        for image in images:
            image_alt = image[0]
            image_link = image[1]

            split_nodes = current_text.split(f"![{image_alt}]({image_link})", 1)
            text_before_image = split_nodes[0]
            text_after_image = split_nodes[1]

            if text_before_image != "":
                node_list.append(TextNode(text_before_image, TextType.TEXT))

            node_list.append(TextNode(image_alt, TextType.IMAGE, image_link))
            
            current_text = text_after_image
        
        if current_text != "":
            node_list.append(TextNode(current_text, TextType.TEXT))

    return node_list


def split_nodes_link(old_nodes):
    node_list = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            node_list.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)

        if links == []:
            node_list.append(old_node)
            continue

        current_text = old_node.text

        for link in links:
            link_text = link[0]
            link = link[1]

            split_nodes = current_text.split(f"[{link_text}]({link})", 1)
            text_before_link = split_nodes[0]
            text_after_link = split_nodes[1]

            if text_before_link != "":
                node_list.append(TextNode(text_before_link, TextType.TEXT))

            node_list.append(TextNode(link_text, TextType.LINK, link))
            
            current_text = text_after_link
        
        if current_text != "":
            node_list.append(TextNode(current_text, TextType.TEXT))

    return node_list


def text_to_textnodes(text):
    node_list = [TextNode(text, TextType.TEXT)]

    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    node_list = split_nodes_delimiter(node_list, "*", TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)

    return node_list


