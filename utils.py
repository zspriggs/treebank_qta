from scipy.stats import chi2_contingency

#makes contingency table so you don't have to do it every time
def chi2(lemma1, total1, lemma2, total2):
    contingency_tbl = [
        [lemma1, total1-lemma1],
        [lemma2, total2-lemma2]
    ]

    #chi2 value, p value, degrees of freedom, expected frequency
    chi2, p, dof, expected = chi2_contingency(contingency_tbl) 

    return chi2, p, dof, expected
