#treebank formatting

#start with
#verb & d.o
#adj/noun agreement?
#object of prep

#Collects all direct objects of a given verb
def collect_verb_dos(verb, words):
    verbs = [w for w in words if w.get('lemma') == 'λέγω' and w.get('postag').startswith('v')]

    objects = [] #rename lol
    for verb in verbs:
        verb_id = verb['id']
        objs = [w for w in words if w['head'] == verb_id and w['relation'] == 'OBJ']
        objects.extend(objs)

    return objects

#Detects if a specific word appears as a do of a given verb
def detect_verb_do(verb, do, words):
    
    return

#Collects all objects of a given preposition
def collect_prep_objs(prep, words):
    return

#Detects if a specific word appears as an object of a given preposition
def detect_prep_obj(prep, do, words):
    return


#further analysis on case, plurality, gender can be done in diff fns
