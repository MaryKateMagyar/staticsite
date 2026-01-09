from enum import Enum
from htmlnode import *
from textnode import *

def markdown_to_blocks(markdown):
    processed_blocks = []
    
    lines = markdown.splitlines()
    current_block_lines = []
    current_is_code = False

    for line in lines:
        if line.startswith("```"):
            if current_is_code:
                block = "\n".join(current_block_lines) + "\n"
                block += "```"
                processed_blocks.append(block)
                current_block_lines = []
                current_is_code = False 
            else:
                if current_block_lines:
                    block = join_lines_into_block(current_block_lines)
                    processed_blocks.append(block)
                    current_block_lines = []
                current_block_lines.append(line)
                current_is_code = True
            
        else:
            if current_is_code:
                current_block_lines.append(line)
            else:
                if line.strip() == "":
                    if current_block_lines:
                        block = join_lines_into_block(current_block_lines)
                        processed_blocks.append(block)
                        current_block_lines = []
                else:
                    current_block_lines.append(line)

    if current_block_lines:
        block = join_lines_into_block(current_block_lines)
        processed_blocks.append(block)

    return processed_blocks

def join_lines_into_block(lines):
    return "\n".join(lines).strip()


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith("> "):
        lines = block.splitlines()
        for line in lines[1:]:
            if not line.startswith("> "):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        lines = block.splitlines()
        for line in lines[1:]:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        lines = block.splitlines()
        count = 2
        for line in lines[1:]:
            if line.startswith(f"{count}. "):
                count += 1
            else:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def block_to_tag(block_type, block=None):
    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            hash_count = block.find(" ")
            return f"h{hash_count}"
        case BlockType.CODE:
            return "pre"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case __:
            raise Exception("block is not a valid block_type")


def list_items_to_html_children_nodes(block, block_type):
    html_children = []
    lines = block.splitlines()

    for line in lines:
        if block_type == BlockType.UNORDERED_LIST:
            stripped_line = line.removeprefix("- ")
        elif block_type == BlockType.ORDERED_LIST:
            prefix = line.find(" ") + 1
            stripped_line = line[prefix:]
        else:
            raise Exception("block is not a list")
        
        children = text_to_children(stripped_line)
        list_node = ParentNode("li", children)
        html_children.append(list_node)
    
    return html_children


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children_nodes = []
    for text_node in text_nodes:
        children_nodes.append(text_node_to_html_node(text_node))
    return children_nodes


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    tag = block_to_tag(block_type, block)

    if block_type == BlockType.UNORDERED_LIST or block_type == BlockType.ORDERED_LIST:
        children = list_items_to_html_children_nodes(block, block_type)
    elif block_type == BlockType.CODE:
        lines = block.splitlines()
        lines = lines[1:]
        lines.pop()
        processed_block = "\n".join(lines) + "\n"
        code_node = TextNode(processed_block, TextType.CODE)
        children = [text_node_to_html_node(code_node)]
    else:
        if block_type == BlockType.PARAGRAPH:
            processed_block = block.replace("\n", " ")
        elif block_type == BlockType.HEADING:
            partition = block.find(" ") + 1
            processed_block = block[partition:]
        elif block_type == BlockType.QUOTE:
            lines = block.splitlines()
            stripped_lines = []
            for line in lines:
                stripped_lines.append(line.removeprefix("> "))
            processed_block = "\n".join(stripped_lines)
        else:
            raise Exception("invalid BlockType")
        
        children = text_to_children(processed_block)

    if children == []:
        children = None

    return ParentNode(tag, children)

        
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(block_to_html_node(block))
    return ParentNode("div", children)

