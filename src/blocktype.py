from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    result = []
    for raw_block in raw_blocks:
        block = raw_block.strip()
        if block:
            result.append(block)

    return result

def is_valid_block(block, prefix):
    if "\n" not in block:
        return True
    lines = block.split("\n")
    for line in lines:
        if line.strip() != "" and not line.lstrip().startswith(prefix):
            return False
    return True    

def block_to_block_type(block):
    if re.match(r"^\s*#{1,6} ", block):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        if is_valid_block(block, ">"):
            return BlockType.QUOTE
    
    if block.startswith("- "):
        if is_valid_block(block, "- "):
            return BlockType.UNORDERED_LIST
    
    if block.startswith("1."):
        split_blocks = [line.strip() for line in block.split("\n") if line.strip()]
        line_number = 0
        for split_block in split_blocks:
            line_number += 1
            if not split_block.startswith(f"{line_number}."):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

