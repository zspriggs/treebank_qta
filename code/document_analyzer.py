
#load document trees
#get keywords
#compare to rest of corpus in various ways (general stats might be useful?)

import stat_calculator as calc
import utils

class document_analyzer:
    def __init__(self, doc_urn):
        try:
            self.data = utils.open_data()
            self.doc_data = self.data[doc_urn]
        except: 
            raise ValueError("Invalid URN")    

        self.urn = doc_urn

    def get_lemma_count(self):
        return len(self.doc_data) - 1

    def get_word_count(self):
        return self.doc_data['TOTAL_WORDS']

    def get_top_lemmas(self, n=10):
        return sorted(self.doc_data.items(), key= lambda x: x[1], reverse=True)[1:(n+1)]

    def get_ttr(self):
        return (len(self.doc_data)-1)/self.doc_data['TOTAL_WORDS']

    def detect_keywords_ll(self, n=10):
        keywords = {}
        for lemma, _ in self.doc_data.items():
            keywords[lemma] = calc.log_likelihood_lemma([self.urn], [], lemma, self.data)

        return sorted(keywords.items(), key=lambda x: x[1]['log likelihood'], reverse=True)[:n]


