#treebank formatting

#start with
#verb & d.o
#adj/noun agreement?
#object of prep

#Collects all direct objects of a given verb
def collect_verb_dos(verb, nodes, children):
    dos = []
    
    for id, node in nodes.items():
        if node.get('lemma') == verb and node.get('postag').startswith('v'):
            for child_id in children.get(id, []):
                child = nodes[child_id]
                if child.get('relation') == 'OBJ':
                    dos.append(child)
    
    return dos

#detects how many times a specific word appears as a do of a given verb
def detect_verb_do(verb, do, nodes, children):
    objects = collect_verb_dos(verb, nodes, children)    
    count = len([1 for object in objects if object.get('lemma') == do])
    
    return count

#how often does this verb take each case
def verb_case_stats(verb, nodes, children):
    dos = collect_verb_dos(verb, nodes, children)
    
    tags = {}
    for word in dos:
        case = tags.get(word.get('postag')[-2], 0)
        tags[case] = case + 1
    
    return tags

#Collects all objects of a given preposition
def collect_prep_objs(prep, words):
    return

#Detects if a specific word appears as an object of a given preposition
def detect_prep_obj(prep, do, words):
    return

def prep_case_stats(prep, do, words):
    return

#further analysis on case, plurality, gender can be done in diff fns
