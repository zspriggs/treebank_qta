from collections import defaultdict
import xml.etree.ElementTree as ET
import os

'''
nodes: {id: Element}
children: {head_id: [child_ids]}
'''
#builds a tree from one sentence
def build_tree(sentence_elem):
    nodes = {} #id, xml element dictionary
    children = defaultdict(list)

    for word in sentence_elem.findall('word'):
        word_id = word.get('id', 0) #these defaults might be bad
        head_id = word.get('head')
        nodes[word_id] = word
        children[head_id].append(word_id)

    return nodes, children

def print_tree(word_map, children, current_id=0, depth=0):
    for child_id in sorted(children[current_id], key=lambda x: int(x)):
        word = word_map[child_id]
        print('  ' * depth + f"{word.get('form')} ({word.get('relation')})")
        print_tree(word_map, children, child_id, depth + 1)
    return

#builds all sent trees for a file
def build_trees(file):
    try:
        tree = ET.parse(file)
    except:
        return
    root = tree.getroot()
    all_trees = []

    for sentence in root.findall('.//sentence'):  # .// to find nested <sentence> elements
        nodes, children = build_tree(sentence)
        all_trees.append((nodes, children))
        
    return all_trees

#builds all trees for all files in a folder
#for now, all combined (not subdivided by doc)
def build_all_trees(folder):
    file_list = os.listdir(folder)
    
    forest = []
    for file in file_list:
        print(f"starting file {file}")
        treeset = build_trees(f"{folder}{file}")
        forest.append(treeset)
        
    return forest

