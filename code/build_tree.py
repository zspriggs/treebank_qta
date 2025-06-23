from collections import defaultdict
import xml.etree.ElementTree as ET

'''
nodes: {id: Element}
children: {head_id: [child_ids]}
'''
def build_tree(sentence_elem):
    nodes = {} #id, xml element dictionary
    children = defaultdict(list)

    for word in sentence_elem.findall('word'):
        word_id = int(word.get('id'))
        head_id = int(word.get('head'))
        nodes[word_id] = word
        children[head_id].append(word_id)

    return nodes, children

def print_tree(word_map, children, current_id=0, depth=0):
    for child_id in sorted(children[current_id], key=lambda x: int(x)):
        word = word_map[child_id]
        print('  ' * depth + f"{word.get('form')} ({word.get('relation')})")
        print_tree(word_map, children, child_id, depth + 1)
    return

def build_trees(file):
    tree = ET.parse(file)
    root = tree.getroot()
    all_trees = []

    for sentence in root.findall('.//sentence'):  # .// to find nested <sentence> elements
        nodes, children = build_tree(sentence)
        all_trees.append((nodes, children))
        
    return all_trees

