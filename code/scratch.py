#use this file for test debug etc

import word_analyzer as wa
from utils import urn_to_name

def main():
    aner = wa.word_analyzer("ἀνήρ")

    print("Calcing top docs")
    raw_lemmas = aner.raw_lemma_freq()
    print(raw_lemmas)
    print([urn_to_name(doc[0]) for doc in raw_lemmas])

    print("Calcing top docs")
    rel_lemmas = aner.rel_lemma_freq()
    print(rel_lemmas)
    print([urn_to_name(doc[0]) for doc in rel_lemmas])

    print("caclcing stats")
    doc = "0012-001.xml"

    
    #print(aner.ll_doc(doc))
    #print(aner.chi2_doc(doc))

#if __name__ == '__main__':
    #main()

def messages(la: wa.word_analyzer):
    print("Calcing top docs, raw frequency")
    raw_lemmas = la.raw_lemma_freq()
    print([f"{urn_to_name(doc[0]) if "ERROR" not in urn_to_name(doc[0]) else "Text Error"}, URN = {doc[0]}, Lemma count = {doc[1]}" for doc in raw_lemmas])

    print("Calcing top docs, relative frequency")
    rel_lemmas = la.rel_lemma_freq()
    print([f"{urn_to_name(doc[0]) if "ERROR" not in urn_to_name(doc[0]) else "Text Error"}, URN = {doc[0]}, Frequency = {doc[1]}" for doc in rel_lemmas])

def document_console_program(la: wa.word_analyzer):
    print("\n*\t*\t*\t*\t*\t*\t*\n")
    print(f"You are analyzing the lemma {la.get_lemma()}")
    print(f"Please provide the document you are interested in inspecting (incl. .xml):")
    URN1 = str(input())
    print(f"Please provide the document you are interested in comparing to (or type \"A\" for all texts:")
    URN2 = str(input())
    #if URN2 == "A":


    print(la.ll([URN1],[] if URN2 == "A" else [URN2]))

    return

def console_program():
    while True:
        print("\n*\t*\t*\t*\t*\t*\t*\n")
        print("Enter lemma or X to stop: ")
        lemma = str(input())

        if lemma == 'X':
            break

        la = wa.word_analyzer(lemma)

        messages(la)

        print("Enter L to enter new lemma, D to enter document mode with current lemma, or X to stop:")
        choice = str(input())

        if choice == "L":
            continue
        elif choice == "D":
            document_console_program(la)
        else: break

console_program()