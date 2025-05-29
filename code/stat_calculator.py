from scipy.stats import chi2_contingency
from scipy.stats import chi2
import utils
import numpy as np
#import pickle

#todo: implement addtl stat tests
#       look into effect size measures


def contingency_table(lemma1, total1, lemma2, total2):
    return [
        [lemma1, total1-lemma1],
        [lemma2, total2-lemma2]
    ]

def chi_squared(lemma1, total1, lemma2, total2):
    #double check this calculation
    contingency_tbl(lemma1, total1, lemma2, total2)

    #chi2 value, p value, degrees of freedom, expected frequency
    chi2, p, dof, expected = chi2_contingency(contingency_tbl)

    return chi2, p, dof, expected

def get_totals(lemma, short_urn, data):
    doc_lemma = data[short_urn][lemma]
    doc_total = data[short_urn]["TOTAL_WORDS"]

    #assumes that document totals are included in corpus totals
    corp_lemma = data["totals"][lemma] - doc_lemma
    corp_total = data["totals"]["TOTAL_WORDS"] - doc_total

    return doc_lemma, doc_total, corp_lemma, corp_total

def chi2_singledoc(lemma, short_urn, data):
    doc_lemma, doc_total, corp_lemma, corp_total = get_totals(lemma, short_urn, data)

    chi2, p, dof, expected = chi2(doc_lemma, doc_total, corp_lemma, corp_total)
    print(f"{doc_lemma} {doc_total} {corp_lemma} {corp_total}")
    print(f"{chi2} , {p}, {dof}, {expected}")

    return chi2, p, dof, expected

#log likelihood preferred for natural language freq data (Dunning 1993, look into this)
#compares document against the rest of the corpus
def ll_singledoc(lemma, short_urn, data):
    #research: diff between results of this and chi2?
    #double check this calculation

    doc_lemma, doc_total, corp_lemma, corp_total = get_totals(lemma, short_urn, data)

    lemmas_total = doc_lemma + corp_lemma
    words_total = doc_total + corp_total

    expected_doc = doc_total * lemmas_total / words_total
    expected_corp = corp_total * lemmas_total / words_total

    doc_non_lemma = doc_total - doc_lemma
    corp_non_lemma = corp_total - corp_lemma

    G = 0
    if doc_lemma > 0:
        G += 2 * doc_lemma * np.log(doc_lemma / expected_doc)
    if corp_lemma > 0:
        G += 2 * corp_lemma * np.log(corp_lemma / expected_corp)
    if doc_non_lemma > 0:
        G += 2 * doc_non_lemma * np.log(doc_non_lemma / (doc_total-expected_doc))
    if corp_non_lemma > 0:
        G += 2 * corp_non_lemma * np.log(corp_non_lemma / (corp_total-expected_corp))

    p1 = doc_lemma / doc_total if doc_total > 0 else 0
    p2 = corp_lemma / corp_total if corp_total > 0 else 0
    log_ratio = np.log2(p1/p2) if p1 > 0 and p2 > 0 else np.nan

    #fac-check that this is okay:
    p_val = chi2.sf(G, df=1)

    return {
        "log likelihood": G,
        "log ratio": log_ratio,
        "p value": p_val
    }

def fischers_singledoc(lemma, short_urn, data):
    #fischers exact test (used for when counts < 5)
    return

def ztest(lemma, short_urn, data):
    #maybe cut this one out
    return

def calc_stats(lemma, short_urn, data_file):
    data = utils.open_data(data_file)
    print(ll_singledoc(lemma, short_urn, data))

calc_stats("ἀνήρ", "0012-001.xml", "testPickle")


