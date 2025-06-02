#super simple just counting up words
import xml.etree.ElementTree as ET
from scipy.stats import chi2_contingency
import os

#TODO: 
#   Put needed logic in stat_calculator, then delete

def get_lemma_totals(file, lemma):
    try:
        tree = ET.parse(file)
    except:
        print(f"Failed to parse {file}. Aborting")
        return 0, 0
    root = tree.getroot()

    lemmas = 0
    words = 0
    for word in root.findall('.//word'):
        words += 1
        if word.get('lemma') == lemma:
            lemmas += 1

    return lemmas, words

def chi_squared_lemma(file1, file2, lemma):
    lemma1_count, word1_count = get_lemma_totals(file1, lemma)
    lemma2_count, word2_count = get_lemma_totals(file2, lemma)

    #chi2 value, p value, degrees of freedom, expected frequency
    chi2, p, dof, expected = chi2(lemma1_count, word1_count, lemma2_count, word2_count) 

    return chi2, p, dof, expected

#makes contingency table so you don't have to do it every time
def chi2(lemma1, total1, lemma2, total2):
    contingency_tbl = [
        [lemma1, total1-lemma1],
        [lemma2, total2-lemma2]
    ]

    #chi2 value, p value, degrees of freedom, expected frequency
    chi2, p, dof, expected = chi2_contingency(contingency_tbl) 

    return chi2, p, dof, expected

#many to many
def chi_squared_m2m(main_fileset, second_fileset, lemma):
    first_lemmas, first_words = 0
    for file in main_fileset:
        temp_lemmas, temp_words = get_lemma_totals(file, lemma)
        first_lemmas += temp_lemmas
        first_words += temp_words

    second_lemmas, second_words = 0
    for file in second_fileset:
        temp_lemmas, temp_words = get_lemma_totals(file, lemma)
        second_lemmas += temp_lemmas
        second_words += temp_words
    
    #chi2, p, dof, expected = chi2(first_lemmas, first_words, second_lemmas, second_words)
    
    return chi2(first_lemmas, first_words, second_lemmas, second_words)

#single to many
def chi_squared_s2m(target_file, target_folder, lemma):
    first_lemmas, first_words = get_lemma_totals(target_file, lemma)

    file_list = os.listdir(target_folder)
    #print(file_list)
    second_lemmas = second_words = 0
    
    for file in file_list:
        rel_path = f"{target_folder}/{file}"
        if rel_path == target_file:
            print("ahhhh no!")
            continue

        temp_lemmas, temp_words = get_lemma_totals(rel_path, lemma)
        second_lemmas += temp_lemmas
        second_words += temp_words

        print(f"Current lemma count: {second_lemmas}")
    
    #chi2, p, dof, expected = chi2(first_lemmas, first_words, second_lemmas, second_words)
    print(f"{first_lemmas} {first_words} {second_lemmas} {second_words}")
    return chi2(first_lemmas, first_words, second_lemmas, second_words)

def main():
    iliad = "../glaux-trees/public/xml/0012-001.xml"
    odyssey = "../glaux-trees/public/xml/0012-002.xml"
    folder = "../glaux-trees/public/xml"

    # print(count_all_words(iliad))
    # print(count_all_words(odyssey))

    # print(count_lemma(iliad, "ἀνήρ"))
    # print(count_lemma(odyssey, "ἀνήρ"))

    lemma = "ἀνήρ"

    # chi2, p = chi_squared_lemma(iliad, odyssey, "ἀνήρ")
    chi2, p, dof, expected = chi_squared_s2m(iliad, folder, "ἀνήρ")

    print(chi2, p)


main()

