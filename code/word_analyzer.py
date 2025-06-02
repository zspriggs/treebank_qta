#idea: take a certain word and generate all the relevant stats
import utils
import stat_calculator as calc

DATA_FILE = "testPickle"

class word_analyzer:
    def __init__(self, lemma: str):
        self.lemma = lemma
        self.data = utils.open_data(DATA_FILE)

    def lemma_freq(self, x = 5):
        sorted_urns = sorted(self.data.keys(), key=lambda k: self.data[k].get(self.lemma, 0), reverse=True)
        return sorted_urns[1:6]

    def ll_doc(self, short_urn: str):
        return calc.log_likelihood_lemma([short_urn], [], self.lemma, self.data)
    
    def chi2_doc(self, short_urn: str):
        return calc.chi_squared_lemma([short_urn], [], self.lemma, self.data)
    
    #fetch appearances of lemma?