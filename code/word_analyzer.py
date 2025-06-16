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
    
    #returns a list of (urn, relative_frequency) tuples ordered by relative frequency
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
    
    #ignores bad URNs (change later?)
    #either calc rel frequency for combined urns or rel freq for everything BUT those urns
    def get_list_rel_freq(self, urns: list, inverse = False):
        lemmas = 0
        total = 0
        if not inverse:
            for urn in urns:
                try: 
                    lemmas += self.data[urn][self.lemma]
                    total += self.data[urn]["TOTAL_WORDS"]
                except: 
                    continue
        else:
            for urn, x in self.data.items():
                if urn not in urns:
                    try: 
                        lemmas += self.data[urn][self.lemma]
                        total += self.data[urn]["TOTAL_WORDS"]
                    except:
                        continue
            
        return lemmas / total if total > 0 else 0

    def get_raw_freq(self, urn):
        try:
            return self.data[urn][self.lemma]
        except:
            return None

    def ll(self, main_urns, comp_urns = []):
        return calc.log_likelihood_lemma(main_urns, comp_urns, self.lemma, self.data)
    
    def chi2(self, main_urns, comp_urns = []):
        return calc.chi_squared_lemma(main_urns, comp_urns, self.lemma, self.data)
    
    def calc_all_stats(self, main_urns, comp_urns = []):
        main_rel_freq = self.get_list_rel_freq(main_urns)
        
        if len(comp_urns) == 0:
            comp_rel_freq = self.get_list_rel_freq(main_urns, inverse = True)
        else:
            comp_rel_freq = self.get_list_rel_freq(comp_urns)
                
        ll = calc.log_likelihood_lemma(main_urns, comp_urns, self.lemma, self.data)
        chi2 = calc.chi_squared_lemma(main_urns, comp_urns, self.lemma, self.data)
        
        return {'main rf': main_rel_freq, 'comp rf': comp_rel_freq, 'll calc': ll, 'chi2 calc': chi2}
        
        
    
    #fetch appearances of lemma?