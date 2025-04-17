import re

from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:

    if is_heading_block(block):
        return BlockType.HEADING
        
    if is_code_block(block):
        return BlockType.CODE
            
    if is_quote_block(block):
        return BlockType.QUOTE

    if is_unordered_list(block):
        return BlockType.UNORDERED_LIST

    if is_ordered_list(block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def is_heading_block(block: str) -> bool:
    heading_regex = r"^#{1,6} "
    heading = re.findall(heading_regex, block)
    if len(heading) > 0:
        return True
    return False

def is_code_block(block: str) -> bool:
    code_regex = r"^```.*```$"
    code = re.findall(code_regex, block)
    if len(code) > 0:
        return True
    return False

def is_quote_block(block: str) -> bool:
    quote_regex = r"^>"
    quote = re.findall(quote_regex, block)
    if len(quote) > 0:
        return True
    return False

def is_unordered_list(block: str) -> bool:
    unordered_regex = r"^- "
    unord_list = block.split('\n')
    count = 0
    for unord in unord_list:
        unordered = re.findall(unordered_regex, unord)
        if len(unordered) > 0:
            count += 1
    if count == len(unord_list):
        return True
    return False

def is_ordered_list(block: str) -> bool:
    ordered_regex = r"^\d\. "
    ord_list = block.split("\n")
    count = 0
    for i in range(len(ord_list)):
        ordered = re.findall(ordered_regex, ord_list[i])
        if len(ordered) > 0:
            if int(ordered[0][0]) == (i + 1):
                count += 1

    if count == len(ord_list):
        return True
    return False