import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from cord19_analysis import create_sample_data, clean_and_prepare_data

# Streamlit app
def main():
    st.title("🦠 CORD-19 Research Papers Explorer")
    st.write("Simple exploration of COVID-19 research papers for Python Frameworks Assignment")
    
    # Load data
    try:
        df = pd.read_csv('data/metadata.csv')
        st.success("✅ Loaded real CORD-19 dataset")
    except:
        df = create_sample_data()
        st.warning("⚠️ Using sample data (real dataset not found in data/metadata.csv)")
    
    # Clean data
    df = clean_and_prepare_data(df)
    
    # Sidebar controls
    st.sidebar.header("📊 Analysis Controls")
    
    # Show basic info
    st.header("Dataset Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Papers", len(df))
    
    with col2:
        st.metric("Columns", len(df.columns))
    
    with col3:
        years = df['year'].unique()
        st.metric("Years Covered", f"{len(years)} years")
    
    # Data preview
    st.subheader("Data Preview")
    st.dataframe(df.head(10))
    
    # Publications by year
    st.subheader("Publications by Year")
    year_counts = df['year'].value_counts().sort_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(year_counts.index, year_counts.values, color='skyblue', alpha=0.7)
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Publications')
    ax.set_title('COVID-19 Research Papers Published Each Year')
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
    
    # Top journals
    st.subheader("Top Publishing Journals")
    journal_counts = df['journal'].value_counts().head(10)
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.barh(journal_counts.index, journal_counts.values, color='lightgreen', alpha=0.7)
    ax2.set_xlabel('Number of Papers')
    ax2.set_title('Top 10 Journals Publishing COVID-19 Research')
    
    st.pyplot(fig2)
    
    # Word frequency
    st.subheader("Common Words in Titles")
    all_titles = ' '.join(df['title'].dropna().astype(str))
    words = all_titles.lower().split()
    from collections import Counter
    word_freq = Counter(words).most_common(15)
    
    words_df = pd.DataFrame(word_freq, columns=['Word', 'Frequency'])
    st.dataframe(words_df)
    
    st.info("💡 **Note**: This is a simplified version for the assignment. With the full dataset, you would see more comprehensive results.")

if __name__ == "__main__":
    main()