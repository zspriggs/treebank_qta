import streamlit as st
import word_analyzer as wa 
import document_analyzer as da
import pandas as pd
import altair as alt
from utils import urn_to_name

##TODO:
#clean up this code!
#add more document analysis
#add explanations to doc analysis

st.set_page_config(layout="wide")

st.html('''
<style>
div[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div {
    max-height: 114px !important; /* Fix the height */
    overflow: auto !important;
}
</style>
''')

st.title("QTA Tools for Greek Treebank")

tab1, tab2, tab3 = st.tabs(["Lemma analyzer", "Document analyzer", "Corpus Overview"])

def create_genre_options():
    """Create genre options for selecting texts by genre"""
    return [
        'Epic poetry', 'Lyric poetry', 'History', 'Tragedy', 'Biography', 'Philosophy',
        'Rhetoric', 'Polyhistory', 'Oratory', 'Epistolography', 'Comedy',
        'Scientific Poetry', 'Philosophic Dialogue', 'Military', 'Biology',
        'Medicine', 'Paradoxography', 'Narrative', 'Dialogue', 'AstronomyAstrology',
        'Geography', 'Physics', 'Language', 'Music', 'Mathematics', 'Mythography',
        'Religious Poetry', 'Theology', 'Engineering', 'Rhetoric',
        'Commentary'
    ]

def display_word_stats(analyzer, main_urns, comparison_urns=[]):
    
    analyzer.lemma = lemma
    #get genre URNS and calculate

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
    elif stats['ll calc']['log likelihood'] == -1:
        st.error("Not enough data to calculate log likelihood. This likely means that there were < 5 lemma occurences in one of the documents.")
    else:
        st.info("No statistically significant difference in frequency detected.")
        
    st.write("Raw data (for debugging):")
    st.write(stats)
            
    with st.expander("What do these numbers mean?"):
        st.markdown("""
        - **Relative Frequency**: How often the word appears, normalized by total word count.
        - **Log-Likelihood** and **Chi-Squared**: Statistical tests for frequency differences.
        - A log-likelihood score > 3.84 generally means that the difference is meaningful. However,
          the difference may be very small, and the effect size (in this app, measured by log ratio) 
          should be considered.
        """)

with tab1: 
    lemma = st.text_input("Enter a lemma to analyze:")
    
    if lemma:
        la = wa.word_analyzer(lemma)
        st.success(f"Analyzing the lemma: {lemma}")
        
        stats_col, comp_col = st.columns(2, gap="large")

        with stats_col:
            st.header("Top Documents by Raw Frequency")
            raw_lemmas = la.raw_freq_list()[:5]
            
            if raw_lemmas[0][1] == 0:
                st.warning("This lemma does not appear in the data. Are you sure it is correct?")
            else:
                raw_data = []
                for urn, count in raw_lemmas:
                    name = urn_to_name(urn)
                    raw_data.append({"Document Name": name, "URN": urn, "Lemma Count": count})
                st.table(pd.DataFrame(raw_data))

                st.header("Top Documents by Relative Frequency")
                rel_lemmas = la.rel_freq_list()[:5]
                rel_data = []
                for urn, count in rel_lemmas:
                    name = urn_to_name(urn)
                    rel_data.append({"Document Name": name, "URN": urn, "Relative Frequency": count})
                st.table(pd.DataFrame(rel_data))
                
                #st.pyplot(la.generate_lineplot())

                st.divider()
                st.subheader("Relative Frequency Lineplot")
                selected_genres = st.multiselect("Select genre(s) to display (all genres are selected by default):", create_genre_options(), default=create_genre_options(), placeholder="Select genre(s)")
                st.pyplot(la.generate_relplot(selected_genres))

                with st.expander("What's this?"):
                    st.write("This line graph shows the relative frequency (raw target lemma count divided by total lemmas) graphed over time for the selected genres, with a 95% confidence interval via bootstrapping.")
                st.divider()

                st.pyplot(la.generate_heatmap())
                with st.expander("What's this?"):
                    st.write("This heatmap displays the relative frequency per genre over time.")
                st.divider()
        with comp_col:
            st.subheader("Compare Documents")

            #allow this to be a list later on (backend already implemented)
            urn1 = st.text_input("Enter URN of the document of interest:", key=1)
            urn2 = st.text_input("Enter URN to compare to (or type 'A' for all texts):", key=2)

            if st.button("Compare"):
                #ADD MORE DATA VIS TO THIS SECTION
                st.spinner("Loading...")
                if urn1:
                    display_word_stats(
                        analyzer=la,
                        main_urns=[urn1],
                        comparison_urns=[] if urn2 == "A" else [urn2]
                    )
                else:
                    st.error("Please enter a valid first URN.")


with tab2:
    doc_urn = st.text_input("Enter URN of the document to inspect:")
    try:
        doc = da.document_analyzer(doc_urn)
    except:
        st.error("Please enter a valid URN")
        st.stop()
    
    if "show_collocates" not in st.session_state:
        st.session_state.show_collocates = False
    if "show_stats" not in st.session_state:
        st.session_state.show_stats = False
        
    col1_, col2_, col3_ = st.columns([5,5,5])
    with col1_:
        stats_clicked = st.button("Get Document Stats")
    with col2_:
        keywords_clicked = st.button("Find keywords")
    with col3_:
        collocates_clicked = st.button("Find Collocates")
        
    if keywords_clicked:
        st.session_state.show_collocates = False
        st.session_state.show_stats = False

        results = doc.detect_keywords_ll(20)
        st.write(f"Document Name: {urn_to_name(doc_urn)}")
        data = []
        for res in results:
            data.append({"Lemma": res[0], "Log likelihood": res[1]['log likelihood'], "Log ratio (direction)": res[1]['log ratio']})
        st.table(pd.DataFrame(data))
        
    if stats_clicked:
        st.session_state.show_stats = True

    if st.session_state.show_stats:
        st.session_state.show_collocates = False

        st.write(f"Total words: {doc.get_word_count()}")
        st.write(f"Unique lemma count: {doc.get_lemma_count()}")
        st.write(f"Type-Token Ratio: {doc.get_ttr()}")
        with st.expander("What's this?"):
            st.write("Type--Token Ratio is the number of unique lemmas divided by the number of total words. This value gives a sense of the lexical complexity of a document.")
        
        st.write(f"Most common lemmas:")

        exclude_stopwords = st.checkbox("Exclude punctuation and stopwords?", value=True)

        results = doc.get_top_lemmas(n=20, exclude_stopwords=exclude_stopwords)

        data = []
        for res in results:
            data.append({"Lemma": res[0], "Raw count": res[1]})
        st.table(pd.DataFrame(data))
        
    if collocates_clicked:
        st.session_state.show_collocates = True

    if st.session_state.show_collocates:
        st.session_state.show_stats = False

        method = st.selectbox(
            "Choose statistical method for collocate detection:",
            options=["chi²", "phi²", "dice coefficient", "mutual information"],
            index=0  # default to chi²
        )
        
        st.write(f"Using: {method}")
        collocates=[]
        if method == "chi²":
            collocates = doc.detect_collocates(method='chi2')
        elif method == "phi²":
            collocates = doc.detect_collocates(method='phi2')
        elif method == "dice coefficient":
            collocates = doc.detect_collocates(method='dice')
        elif method == "mutual information":
            collocates = doc.detect_collocates(method='mi')          
            
        data=[]
        for collocate in collocates:
            data.append({"Word": collocate[0][0], "Collocate": collocate[0][1], "Score": collocate[1]})
        st.table(pd.DataFrame(data))
        
with tab3:
    st.write("work in progress")
