'''
TODO: 
adj/noun agreement stuff
more complex syntax features (hard coded? or incorporate flexibility somehow?)
add capability to return contexts (w citations!) instead of just words/counts
add capability to base on forms rather than only lemmas
'''
#Collects all direct objects of a given verb
def collect_verb_dos(verb, nodes, children, lemma_mode = True):
    dos = []
    
    for id, node in nodes.items():
        if (lemma_mode and node.get('lemma') == verb) or (not lemma_mode and node.get('form') == verb) \
            and node.get('postag').startswith('v'):

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

# !! might need to flip??
def collect_prep_objs(prep, nodes, children):
    objects = []
    for id, node in nodes.items():
        if node.get('lemma') == prep and node.get('postag').startswith('r') and node.get('relation') == "AuxP":
            for child_id in children:
                child = nodes[child_id]
                relation = child.get('relation')
                if relation == "ATR" or relation == "OBJ" or relation == "ADV":
                    objects.append(child)

    return objects

#Detects if a specific word appears as an object of a given preposition
def detect_prep_obj(prep, obj, nodes, children):
    objects = collect_prep_objs(prep, nodes, children)    
    count = len([1 for object in objects if object.get('lemma') == obj])
    
    return count 

def prep_case_stats(prep, obj, nodes, children):
    objs = collect_prep_objs(prep, nodes, children)
    
    tags = {}
    for word in objs:
        case = tags.get(word.get('postag')[-2], 0)
        tags[case] = case + 1
    
    return tags


#further analysis on case, plurality, gender can be done in diff fns
