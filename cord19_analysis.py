import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import re

# Since the real dataset is huge, let's create a sample for demonstration
def create_sample_data():
    """Create sample COVID-19 research data for the assignment"""
    data = {
        'title': [
            'COVID-19 transmission dynamics and control',
            'Vaccine efficacy against SARS-CoV-2 variants',
            'Social distancing impact on pandemic spread',
            'Treatment options for severe COVID-19 cases',
            'Long-term effects of coronavirus infection',
            'Mask effectiveness in preventing transmission',
            'Economic impact of lockdown measures',
            'Mental health during pandemic isolation',
            'Remote learning challenges during COVID',
            'Healthcare system capacity during surges'
        ],
        'publish_time': [
            '2020-03-15', '2021-02-20', '2020-06-10', '2020-08-05', '2021-05-12',
            '2020-04-22', '2020-07-30', '2020-09-18', '2020-11-05', '2021-01-08'
        ],
        'journal': [
            'Lancet', 'Nature Medicine', 'JAMA', 'BMJ', 'NEJM',
            'CDC Report', 'Health Economics', 'Psychiatry Research', 'Education Journal', 'Healthcare Management'
        ],
        'abstract': [
            'Study of transmission patterns and control measures',
            'Analysis of vaccine effectiveness against new variants',
            'Impact of social distancing on infection rates',
            'Review of treatment protocols for severe cases',
            'Examination of long COVID symptoms and effects',
            'Evaluation of mask usage in public spaces',
            'Economic consequences of pandemic restrictions',
            'Mental health trends during lockdown periods',
            'Challenges in remote education delivery',
            'Hospital capacity management strategies'
        ]
    }
    return pd.DataFrame(data)

def load_and_explore_data():
    """Part 1: Data Loading and Basic Exploration"""
    print("=== PART 1: DATA LOADING AND EXPLORATION ===")
    
    # Try to load real data, fall back to sample
    try:
        df = pd.read_csv('data/metadata.csv')
        print("✅ Loaded real CORD-19 dataset")
    except:
        df = create_sample_data()
        print("⚠️ Using sample data (real dataset not found)")
    
    # Basic exploration
    print(f"\nDataset shape: {df.shape}")
    print(f"\nFirst few rows:")
    print(df.head())
    
    print(f"\nData types:")
    print(df.dtypes)
    
    print(f"\nMissing values:")
    print(df.isnull().sum())
    
    return df

def clean_and_prepare_data(df):
    """Part 2: Data Cleaning and Preparation"""
    print("\n=== PART 2: DATA CLEANING AND PREPARATION ===")
    
    # Handle dates
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    
    # Fill missing years with 2020 (most common COVID year)
    df['year'].fillna(2020, inplace=True)
    
    # Create abstract word count
    df['abstract_word_count'] = df['abstract'].str.split().str.len()
    
    print("✅ Data cleaning completed")
    print(f"Years in data: {df['year'].unique()}")
    
    return df

def analyze_and_visualize(df):
    """Part 3: Data Analysis and Visualization"""
    print("\n=== PART 3: DATA ANALYSIS AND VISUALIZATION ===")
    
    # Create visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Publications over time
    year_counts = df['year'].value_counts().sort_index()
    axes[0,0].bar(year_counts.index, year_counts.values, color='skyblue')
    axes[0,0].set_title('Publications by Year')
    axes[0,0].set_xlabel('Year')
    axes[0,0].set_ylabel('Number of Papers')
    
    # 2. Top journals (using sample data)
    journal_counts = df['journal'].value_counts().head(10)
    axes[0,1].barh(journal_counts.index, journal_counts.values, color='lightgreen')
    axes[0,1].set_title('Top Publishing Journals')
    axes[0,1].set_xlabel('Number of Papers')
    
    # 3. Word frequency in titles
    all_titles = ' '.join(df['title'].dropna())
    words = re.findall(r'\b\w+\b', all_titles.lower())
    word_freq = Counter(words).most_common(10)
    
    words, counts = zip(*word_freq)
    axes[1,0].bar(words, counts, color='orange')
    axes[1,0].set_title('Most Common Words in Titles')
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # 4. Abstract word count distribution
    axes[1,1].hist(df['abstract_word_count'].dropna(), bins=10, color='purple', alpha=0.7)
    axes[1,1].set_title('Abstract Word Count Distribution')
    axes[1,1].set_xlabel('Word Count')
    axes[1,1].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig('analysis_results.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Paper Titles')
    plt.savefig('wordcloud.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Analysis and visualizations completed")

def main():
    """Run the complete analysis"""
    print("🦠 CORD-19 DATA ANALYSIS ASSIGNMENT")
    print("=" * 50)
    
    df = load_and_explore_data()
    df = clean_and_prepare_data(df)
    analyze_and_visualize(df)
    
    print("\n✅ ASSIGNMENT COMPLETED SUCCESSFULLY!")
    print("📊 Check the generated visualizations:")
    print("   - analysis_results.png")
    print("   - wordcloud.png")

if __name__ == "__main__":
    main()