from textnode import TextNode, TextType

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
