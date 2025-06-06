import utils
import stat_calculator as calc

DATA_FILE = "treebankData"

class word_analyzer:
    def __init__(self, lemma: str):
        self.lemma = lemma
        self.data = utils.open_data(DATA_FILE)

    def get_lemma(self):
        return self.lemma

    def raw_lemma_freq(self):
        urn_counts = []
        for urn, lemma_counts in self.data.items():
            raw_freq = lemma_counts.get(self.lemma,0)
            urn_counts.append((urn, raw_freq))

        return sorted(urn_counts, key = lambda urn_tuple: urn_tuple[1], reverse=True)[1:]
        
    def rel_lemma_freq(self):
        urn_counts = []
        for urn, lemma_counts in self.data.items():
            rel_freq = lemma_counts.get(self.lemma,0)/lemma_counts["TOTAL_WORDS"]
            urn_counts.append((urn, rel_freq))

        return sorted(urn_counts, key = lambda urn_tuple: urn_tuple[1], reverse=True)[1:]

    def get_rel_freq(self, urn):
        try: 
            return self.data[urn][self.lemma]/self.data[urn]["TOTAL_WORDS"]
        except: 
            return None

    def get_raw_freq(self, urn):
        try:
            return self.data[urn][self.lemma]
        except:
            return None

    def ll(self, main_urns, comp_urns = []):
        return calc.log_likelihood_lemma(main_urns, comp_urns, self.lemma, self.data)
    
    def chi2(self, main_urns, comp_urns = []):
        return calc.chi_squared_lemma(main_urns, comp_urns, self.lemma, self.data)
    
    #fetch appearances of lemma?