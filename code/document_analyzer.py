import stat_calculator as calc
import utils
import os
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

#TODO: Explanatory comments for functions

class document_analyzer:
    def __init__(self, doc_urn):
        try:
            self.data = utils.open_data()
            self.doc_data = self.data[doc_urn]

            this_dir = os.path.dirname(__file__)
            xml_file = os.path.join(this_dir, "data", "xml", f"{doc_urn}.xml")

            self.text = utils.extract_text(xml_file)
        except: 
            raise ValueError("Invalid URN")    

        self.urn = doc_urn

    def get_lemma_count(self):
        return len(self.doc_data) - 1

    def get_word_count(self):
        return self.doc_data['TOTAL_WORDS']

    def get_top_lemmas(self, n=10, exclude_stopwords=True):
        sorted_lemmas = sorted(self.doc_data.items(), key= lambda x: x[1], reverse=True)

        if exclude_stopwords:
            file_content = utils.read_stopwords()
            stopwords = []
            for line in file_content:
                if not("#" in line or len(line) == 0 or line.isspace()):
                    stopwords.append(line.strip())
            return [word for word in sorted_lemmas if word[0] not in stopwords][1:(n+1)]
        
        return sorted_lemmas[1:(n+1)]

    def get_ttr(self):
        return (len(self.doc_data)-1)/self.doc_data['TOTAL_WORDS']

    def detect_keywords_ll(self, n=10):
        keywords = {}
        for lemma, _ in self.doc_data.items():
            keywords[lemma] = calc.log_likelihood_lemma([self.urn], [], lemma, self.data)

        #sort by biggest/smallest log ratio
        return sorted(keywords.items(), key=lambda x: abs(int(x[1]['log ratio'])), reverse=True)[:n] 
    
    
    def detect_collocates(self, method='chi2', n=10):
        """
        Detects top n collocates in a document, using specified NLTK function.
        If n is 0, all collocates will be returned
        """
        
        finder = BigramCollocationFinder.from_words(self.text)
        finder.apply_freq_filter(3)

        if method == 'chi2':
            scored = finder.score_ngrams(BigramAssocMeasures.chi_sq)
        elif method == 'phi2':
            scored = finder.score_ngrams(BigramAssocMeasures.phi_sq)
        elif method == 'dice':
            scored = finder.score_ngrams(BigramAssocMeasures.dice)
        elif method == 'mi':
            scored = finder.score_ngrams(BigramAssocMeasures.mi_like)
            
        if n == 0: n = len(scored)

        return sorted(scored, key=lambda x: x[1], reverse=True)[:n]
