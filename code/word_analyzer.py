import utils
import stat_calculator as calc
import pandas as pd
import seaborn as sns
import altair as alt


class word_analyzer:
    def __init__(self, lemma: str):
        self.lemma = lemma
        self.data = utils.open_data()

    def get_lemma(self):
        return self.lemma

    def raw_freq_list(self):
        urn_counts = []
        for urn, lemma_counts in self.data.items():
            raw_freq = lemma_counts.get(self.lemma,0)
            urn_counts.append((urn, raw_freq))

        return sorted(urn_counts, key = lambda urn_tuple: urn_tuple[1], reverse=True)[1:]
    
    #returns a list of (urn, relative_frequency) tuples ordered by relative frequency
    def rel_freq_list(self):
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
    def combined_rel_freq(self, urns: list, inverse = False):
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
        return self.data[urn].get(self.lemma, 0)

    def ll(self, main_urns, comp_urns = []):
        return calc.log_likelihood_lemma(main_urns, comp_urns, self.lemma, self.data)
    
    def chi2(self, main_urns, comp_urns = []):
        return calc.chi_squared_lemma(main_urns, comp_urns, self.lemma, self.data)
    
    def calc_all_stats(self, main_urns, comp_urns = []):
        main_rel_freq = self.combined_rel_freq(main_urns)
        
        if len(comp_urns) == 0:
            comp_rel_freq = self.combined_rel_freq(main_urns, inverse = True)
        else:
            comp_rel_freq = self.combined_rel_freq(comp_urns)
                
        ll = calc.log_likelihood_lemma(main_urns, comp_urns, self.lemma, self.data)
        chi2 = calc.chi_squared_lemma(main_urns, comp_urns, self.lemma, self.data)
        
        return {'main rf': main_rel_freq, 'comp rf': comp_rel_freq, 'll calc': ll, 'chi2 calc': chi2}
    
    def graph(self):
        csv_path = "./data/matched_urns.csv"
        df = pd.read_csv(csv_path, dtype={"URN": str})
        
        #data_dict = utils.open_data()                
            
        df["raw freq"] = df.apply(lambda row: self.get_raw_freq(row.URN), axis=1)
        df["rel freq"] = df.apply(lambda row: self.get_rel_freq(row.URN), axis=1)
        df["century"] = df["Date"].apply(utils.clean_century)
                    
        plot = sns.lineplot(
            data=df,
            x='century',
            y='rel freq',
            errorbar=('ci',95)  # built-in bootstrap CI
        )
        fig = plot.get_figure()
        
        return fig #??
        #fig.savefig("out.png") 
        
        
    #def find_collocates():
        #return   
    
    #fetch appearances of lemma?