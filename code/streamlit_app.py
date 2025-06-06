import streamlit as st
import word_analyzer as wa 
import pandas as pd
from utils import urn_to_name, ll_comprehender

st.title("Lemma Analyzer App")

# Lemma input
lemma = st.text_input("Enter a lemma to analyze:")

if lemma:
    la = wa.word_analyzer(lemma)
    st.success(f"Analyzing the lemma: {lemma}")

    st.header("Top Documents by Raw Frequency")
    raw_lemmas = la.raw_lemma_freq()[:5]
    raw_data = []
    for urn, count in raw_lemmas:
        name = urn_to_name(urn)
        raw_data.append({"Document Name": name, "URN": urn, "Lemma Count": count})
    st.table(pd.DataFrame(raw_data))

    st.header("Top Documents by Relative Frequency")
    rel_lemmas = la.rel_lemma_freq()[:5]
    rel_data = []
    for urn, count in rel_lemmas:
        name = urn_to_name(urn)
        rel_data.append({"Document Name": name, "URN": urn, "Raw Frequency": count})
    st.table(pd.DataFrame(rel_data))

    st.divider()

    # Document comparison mode
    st.subheader("Compare Documents")

    urn1 = st.text_input("Enter URN of the document to inspect:")
    urn2 = st.text_input("Enter URN to compare to (or type 'A' for all texts):")

    if st.button("Compare"):
        if urn1:
            comparison_result = la.ll([urn1], [] if urn2 == "A" else [urn2])
            st.write("Comparison result:")
            st.write(comparison_result)
            st.write(ll_comprehender(comparison_result))
        else:
            st.error("Please enter a valid first URN.")