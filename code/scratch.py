#use this file for test debug etc

import word_analyzer as wa
import detect_grammar as g
import build_tree
from utils import urn_to_name
import time

def main():
    file = "../xml/0012-001.xml"
    verb = "τεύχω"
    trees = build_tree.build_trees(file)
    #print(trees)
    for tree in trees:
        dos = g.collect_verb_dos(verb, tree[0], tree[1])
        for do in dos:
            print(do.get('form'), do.get('lemma'), do.get('postag'))


start_time = time.time()
main()
print("took %s seconds to detect lemma in doc " % (time.time() - start_time))

