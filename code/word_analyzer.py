#idea: take a certain word and generate all the relevant stats
import utils
import stat_calculator

DATA_FILE = "testPickle"

class word_analyzer:
    def __init__(self, lemma: str):
        self.lemma = lemma
        self.data = utils.open_data(DATA_FILE)

    def lemma_freq(self, x = 5):
        #this is gonna take forever prolly
        sorted_lemmas = sorted(map(lambda d: d.get(self.lemma, 0), self.data.values()))
        return sorted_lemmas[-5:]

    def ll_doc(self, short_urn: str):
        return stat_calculator.ll_singledoc(self.lemma, short_urn, self.data)
    
    def chi2_doc(self, short_urn: str):
        return stat_calculator.chi2_singledoc(self.lemma, short_urn, self.data)
    
    #fetch appearances of lemma?