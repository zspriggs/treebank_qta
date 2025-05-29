from collections import defaultdict
import xml.etree.ElementTree as ET

tree = ET.parse("../glaux-trees/public/xml/0627-025.xml")
root = tree.getroot()

def build_dependency_tree(sentence_elem):
    nodes = {} #id, xml element dictionary
    children = defaultdict(list)

    for word in sentence_elem.findall('word'):
        word_id = int(word.get('id'))
        head_id = int(word.get('head'))
        nodes[word_id] = word
        children[head_id].append(word_id)

    return nodes, children

# Example: build for first sentence
sentence = root.find('sentence')
nodes, children = build_dependency_tree(sentence)

for value in nodes.values():
    #print(value.get('lemma'))
    print(value.attrib)
