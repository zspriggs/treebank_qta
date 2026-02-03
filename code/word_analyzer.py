import utils
import stat_calculator as calc
import pandas as pd
import seaborn as sns

import document_analyzer as da
import networkx as nx
import matplotlib.pyplot as plt

from utils import urn_to_name

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
    
    #ignores bad URNs
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
    
    def generate_lineplot(self):
        df = utils.read_metadata()

        df["Relative Frequency"] = df.apply(lambda row: self.get_rel_freq(row.URN), axis=1)
        df["Century"] = df["Date"].apply(utils.clean_century)
                    
        plot = sns.lineplot(
            data=df,
            x='Century',
            y='Relative Frequency',
            errorbar=('ci',95)  # bootstrap confidence interval
        )
        plot.set_title(f"Relative Frequency of {self.lemma} Over Time")
        fig = plot.get_figure()
        
        return fig
    
    def generate_pichart(self, n=5):
        df = utils.read_metadata()
        df['Raw Frequency'] = df.apply(lambda row: self.get_raw_freq(row.URN), axis=1)
        print(df)
        
        #get top 5 for rel freq
        sorted_df = df.sort_values(by=['Raw Frequency'], axis=0, ascending=False)
        print(sorted_df)
        pie_data = sorted_df.head(n)['Raw Frequency'].tolist()
        print(pie_data)
        pie_labels = sorted_df.head(n)['Title'].tolist()

        #add sum of all others
        pie_data.append(sorted_df.tail(-1 * n)['Raw Frequency'].sum())
        pie_labels.append("Other")

        if pie_data[-1] > pie_data[1] * 10: 
            print(pie_data[-1], pie_data[1])
            return

        colors = sns.color_palette('pastel')
        plot = plt.pie(pie_data, labels=pie_labels, colors=colors)
        plt.title(f"Raw frequency of {self.lemma} per document")
        fig = plt.gcf()

        return fig

    def generate_heatmap(self):
        df = utils.read_metadata()

        df["Relative Frequency"] = df.apply(lambda row: self.get_rel_freq(row.URN), axis=1)
        df["Century"] = df["Date"].apply(utils.clean_century)

        grouped = (
            df.groupby(['Century', 'Genre'])
            .agg(
                mean_rel_freq=('Relative Frequency', 'mean'),
                std_rel_freq=('Relative Frequency', 'std'),
                num_docs=('Relative Frequency', 'count')
            )
            .reset_index()
        )

        pivoted = grouped.pivot(index='Century', columns='Genre', values='mean_rel_freq')
        plot = sns.heatmap(pivoted)
        plot.set_title(f"{self.lemma} Relative Frequency Heatmap")

        fig = plot.get_figure()

        return fig

    def generate_relplot(self, genres):
        df = utils.read_metadata()

        df["Relative Frequency"] = df.apply(lambda row: self.get_rel_freq(row.URN), axis=1)
        df["Century"] = df["Date"].apply(utils.clean_century)

        df = df[df['Genre'].isin(genres)]

        plot = sns.relplot(
            data=df,
            x="Century", y="Relative Frequency", kind="line")

        return plot

    def graph_collocates_in_doc(self, urn):
        doc = da.document_analyzer(urn)
        collocates = doc.detect_collocates(n=0)
        
        stopwords = utils.read_stopwords()
        lemma_collocates = [(w1, w2, score) for (w1, w2), score in collocates if (w1 == self.lemma or w2 == self.lemma) and (w1 not in stopwords and w2 not in stopwords)]
        df = pd.DataFrame(lemma_collocates, columns=["Word1", "Word2", "Score"])
            
        G=nx.from_pandas_edgelist(df, 'Word1', 'Word2', 'Score')
        fig, ax = plt.subplots(figsize=(10, 8))
        pos = nx.spring_layout(G, k=5, iterations=50, weight='Score')
        nx.draw_networkx(G, with_labels=True, pos=pos, node_color="lightgreen", edge_color="lightgreen", font_size=8, ax=ax)
        
        plt.title(f"Collocates of {self.lemma} in {utils.urn_to_name(urn)} (excluding stopwords)")

        plot = fig.get_figure()
        
        return plot
