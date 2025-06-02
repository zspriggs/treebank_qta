#use this file for test debug etc

import word_analyzer as wa

def main():
    print("what")
    aner = wa.word_analyzer("ἀνήρ")

    print("Calcing top docs")
    print(aner.lemma_freq())

    print("caclcing stats")
    doc = "0012-001.xml"

    
    #print(aner.ll_doc(doc))
    #print(aner.chi2_doc(doc))

if __name__ == '__main__':
    main()