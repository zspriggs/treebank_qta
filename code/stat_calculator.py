from scipy.stats import chi2_contingency
from scipy.stats import chi2
import numpy as np

#todo: implement addtl stat tests
#       look into effect size measures
#       double check current test logic and results

def contingency_table(lemma1, total1, lemma2, total2):
    return [
        [lemma1, total1-lemma1],
        [lemma2, total2-lemma2]
    ]

#assumes no list overlap between first_urns and second_urns (change this for robustness later)
#ignores bad urns
#if second_urns is passed empty, then first_urns are comapred against whole corpus
def get_totals(first_urns: list, second_urns: list, lemma: str, data):
    if len(first_urns) == 0:
        print("No document(s) given.")
        return
    
    lemma1 = lemma2 = total1 = total2 = 0
    for urn in first_urns:
        try:
            lemma1 += data[urn][lemma]
            total1 += data[urn]["TOTAL_WORDS"]
        except:
            continue

    if len(second_urns) == 0: #If we want to compare the first list against all the lemmas
        lemma2 = data["totals"][lemma] - lemma1
        total2 = data["totals"]["TOTAL_WORDS"] - total1
    else:
        for urn in second_urns: 
            try:
                lemma2 += data[urn][lemma]
                total2 += data[urn]["TOTAL_WORDS"]
            except: 
                continue

    if lemma1 < 5 or lemma2 < 5 or total1 < 5 or total2 < 5:
        print("Not enough data. May be caused by a rare lemma, or a bad URN")
        return 0, 0, 0, 0
    
    return lemma1, total1, lemma2, total2

def chi_squared_lemma(first_urns: list, second_urns: list, lemma: str, data):
    lemma1, total1, lemma2, total2 = get_totals(first_urns, second_urns, lemma, data)
    if lemma1 == 0: #if lemma1 == 0, it means one or all values were < 5
        return None
    return calc_chi_squared(lemma1, total1, lemma2, total2)

def log_likelihood_lemma(first_urns: list, second_urns: list, lemma: str, data):
    lemma1, total1, lemma2, total2 = get_totals(first_urns, second_urns, lemma, data)
    if lemma1 == 0:  #if lemma1 == 0, it means one or all values were < 5
        return None
    return calc_log_likelihood(lemma1, total1, lemma2, total2)

def calc_chi_squared(var1, total1, var2, total2):
    table = contingency_table(var1, total1, var2, total2)
    
    #chi2 value, p value, degrees of freedom, expected frequency
    chi2, p, dof, expected = chi2_contingency(table)

    return {
        "chi squared": chi2,
        "p value": p,
        "dof": dof, 
        "expected frequency": expected }
    

#log likelihood preferred for natural language freq data (Dunning 1993, look into this)
#compares two lingustic features
def calc_log_likelihood(var1, total1, var2, total2):
    print("TEST DATA:")
    print(var1, total1, var2, total2)
    #TODO:
    #research: diff between results of this and chi2?
    #double check this calculation

    vars_total = var1 + var2
    all_total = total1 + total2

    expected_total1 = total1 * vars_total / all_total
    expected_total2 = total2 * vars_total / all_total

    non_occurence1 = total1 - var1
    non_occurence2 = total2 - var2

    G = 0
    if var1 > 0:
        G += 2 * var1 * np.log(var1 / expected_total1)
    if var2 > 0:
        G += 2 * var2 * np.log(var2 / expected_total2)
    if non_occurence1 > 0:
        G += 2 * non_occurence1 * np.log(non_occurence1 / (total1-expected_total1))
    if non_occurence2 > 0:
        G += 2 * non_occurence2 * np.log(non_occurence2 / (total2-expected_total2))

    p1 = var1 / total1 if total1 > 0 else 0
    p2 = var2 / total2 if total2 > 0 else 0
    log_ratio = np.log2(p1/p2) if p1 > 0 and p2 > 0 else np.nan

    #fac-check that this is okay:
    p_val = chi2.sf(G, df=1)

    return {
        "log likelihood": G,
        "log ratio": log_ratio,
        "p value": p_val
    }

def calc_fischers():
    #fischers exact test (used for when counts < 5)
    return

def calc_ztest():
    #maybe cut this one out
    return

#def calc_stats(lemma, short_urn, data_file):
    #data = utils.open_data(data_file)
    #print(ll_singledoc(lemma, short_urn, data))

#calc_stats("ἀνήρ", "0012-001.xml", "testPickle")'''


