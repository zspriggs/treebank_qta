import streamlit as st
import word_analyzer as wa 
import pandas as pd
import altair as alt
from utils import urn_to_name

st.title("Lemma Analyzer App")


def display_word_stats(analyzer, main_urns, comparison_urns=[]):
    
    analyzer.lemma = lemma 
    stats = analyzer.calc_all_stats(main_urns, comparison_urns)
    
    if stats['ll calc'] == None or stats['chi2 calc'] == None:
        st.error("Error running analysis. May be due to a the lemma being rare (< 5 occurences) " +
                 "in the text, or a bad URN.")
        return

    #currently only single-doc support
    doc = urn_to_name(main_urns[0])
    comparison = urn_to_name(comparison_urns[0]) if len(comparison_urns) > 0 else "All documents"
    st.header(f"📊 Stats for '{lemma}' in {doc}")

    freq_data = pd.DataFrame({
        'Group': [doc, comparison],
        'Relative Frequency': [stats['main rf'], stats['comp rf']]
    })

    chart = alt.Chart(freq_data).mark_bar().encode(
        x='Group',
        y='Relative Frequency',
        color='Group',
        tooltip=['Group', 'Relative Frequency']
    ).properties(
        title="Relative Frequency Comparison"
    )

    st.altair_chart(chart, use_container_width=True)

    # === Significance Metrics ===
    col1, col2 = st.columns(2)
    col1.metric("Log-Likelihood", round(stats['ll calc']['log likelihood'], 2))
    col2.metric("Chi-Squared", round(stats['chi2 calc']['chi squared'], 2))

    if stats['ll calc']['log likelihood'] > 3.84:
        st.success("The log likelihood is greater than 3.84, meaning that the difference between" + 
                   " word usage is statistically significant (p < 0.05).")
        log_ratio = stats['ll calc']['log ratio']        
        if log_ratio is None:
            st.write("Effect size unavailable")
        else:
            factor = 2 ** abs(log_ratio)

            if log_ratio > 0:
                st.success(f"The log ratio is {log_ratio}, meaning that the lemma {lemma} is used " +
                           f"{factor:.2f}× more often in {doc} than in {comparison}")
            elif log_ratio < 0:
                st.success(f"The log ratio is {log_ratio}, meaning that the lemma {lemma} is used " +
                           f"{factor:.2f}× more often in {comparison} than in {doc}")
            else:
                st.info(f"The log ratio is {log_ratio}, meaning that the lemma {lemma} is used " + 
                        f"equally often in {doc} and {comparison}")
    else:
        st.info("No statistically significant difference in frequency detected.")
        
    st.write("Raw data (for debugging):")
    st.write(stats)
            
    with st.expander("📘 What do these numbers mean?"):
        st.markdown("""
        - **Relative Frequency**: How often the word appears, normalized by total word count.
        - **Log-Likelihood** and **Chi-Squared**: Statistical tests for frequency differences.
        - A log-likelihood score > 3.84 generally means that the difference is meaningful. However,
          the difference may be very small, and the effect size (in this app, measured by log ratio) 
          should be considered.
        """)


# Lemma input
lemma = st.text_input("Enter a lemma to analyze:")

if lemma:
    la = wa.word_analyzer(lemma)
    st.success(f"Analyzing the lemma: {lemma}")

    st.header("Top Documents by Raw Frequency")
    raw_lemmas = la.raw_lemma_freq()[:5]
    
    if raw_lemmas[0][1] == 0:
        st.warning("This lemma does not appear in the data. Are you sure it is correct?")
    else:
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
            rel_data.append({"Document Name": name, "URN": urn, "Relative Frequency": count})
        st.table(pd.DataFrame(rel_data))

        st.divider()

        # Document comparison mode
        st.subheader("Compare Documents")

        #allow this to be a list later on (backend already implemented)
        urn1 = st.text_input("Enter URN of the document to inspect:")
        urn2 = st.text_input("Enter URN to compare to (or type 'A' for all texts):")

        if st.button("Compare"):
            st.spinner("Loading...")
            if urn1:
                display_word_stats(
                    analyzer=la,
                    main_urns=[urn1],
                    comparison_urns=[] if urn2 == "A" else [urn2]
                )
            else:
                st.error("Please enter a valid first URN.")
