# sentiment_visualization.py

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from textblob import TextBlob
import random

def get_review_sample_from_chunks(file_path, sample_size=50_000, chunk_size=200_000, random_state=42):
    """
    Reads a large CSV in chunks and collects a random sample of reviews
    without loading the entire file into memory.

    Parameters:
    - file_path: Path to the raw CSV data.
    - sample_size: The total number of reviews you want in your final sample.
    - chunk_size: The number of rows to read into memory at a time.
    - random_state: Seed for reproducibility.

    Returns:
    - A pandas DataFrame containing the sampled reviews.
    """
    print(f"Starting to sample {sample_size} reviews from {file_path}...")
    
    # Set the random seed for pandas sampling
    random.seed(random_state)
    
    chunk_iterator = pd.read_csv(
        file_path,
        chunksize=chunk_size,
        usecols=['review/text'] # Only load the text column
    )
    
    sampled_chunks = []
    total_sampled = 0
    
    for i, chunk in enumerate(chunk_iterator):
        print(f"Processing chunk {i+1}...")
        chunk.dropna(inplace=True)
        
        # Determine how many more samples we need
        needed = sample_size - total_sampled
        if needed <= 0:
            break # We have enough samples

        # Determine how many to take from this chunk
        take_from_chunk = min(needed, len(chunk))
        
        # Take a random sample from the current chunk
        sampled_chunks.append(chunk.sample(n=take_from_chunk, random_state=random_state))
        total_sampled += take_from_chunk

    print(f"Finished sampling. Total reviews collected: {total_sampled}")
    
    if not sampled_chunks:
        return pd.DataFrame(columns=['review/text'])
        
    return pd.concat(sampled_chunks)

def generate_sentiment_wordclouds(reviews_df):
    """
    Analyzes sentiment of reviews in a DataFrame and generates word clouds.
    """
    if reviews_df.empty or 'review/text' not in reviews_df.columns:
        print("Input DataFrame is empty or missing 'review/text' column.")
        return

    print("Calculating sentiment for sampled reviews... (This may take a few minutes)")
    
    # Define a simple function to get sentiment polarity
    def get_sentiment(text):
        # Using try-except to handle potential errors with non-string data
        try:
            return TextBlob(str(text)).sentiment.polarity
        except:
            return 0.0

    reviews_df['sentiment'] = reviews_df['review/text'].apply(get_sentiment)

    # Define sentiment thresholds
    positive_threshold = 0.15
    negative_threshold = -0.15

    # Combine all reviews for each category into a single string
    # Add common "stopwords" to the set to be ignored
    custom_stopwords = set(STOPWORDS) | {'book', 'read', 'reading', 'story', 'books'}

    # --- Positive Word Cloud ---
    positive_text = " ".join(review for review in reviews_df[reviews_df['sentiment'] > positive_threshold]['review/text'])
    
    if positive_text.strip():
        print("Generating Positive Reviews Word Cloud...")
        pos_wc = WordCloud(width=800, height=400, background_color='white', stopwords=custom_stopwords).generate(positive_text)
        
        plt.figure(figsize=(12, 6))
        plt.imshow(pos_wc, interpolation='bilinear')
        plt.axis("off")
        plt.title("Positive Reviews Word Cloud", fontsize=16)
        plt.show()
    else:
        print("No positive reviews found to generate a word cloud.")

    # --- Negative Word Cloud ---
    negative_text = " ".join(review for review in reviews_df[reviews_df['sentiment'] < negative_threshold]['review/text'])

    if negative_text.strip():
        print("Generating Negative Reviews Word Cloud...")
        neg_wc = WordCloud(width=800, height=400, background_color='black', colormap='Reds', stopwords=custom_stopwords).generate(negative_text)

        plt.figure(figsize=(12, 6))
        plt.imshow(neg_wc, interpolation='bilinear')
        plt.axis("off")
        plt.title("Negative Reviews Word Cloud", fontsize=16)
        plt.show()
    else:
        print("No negative reviews found to generate a word cloud.")


if __name__ == "__main__":
    # You might need to install these libraries first:
    # pip install wordcloud
    # pip install textblob
    # python -m textblob.download_corpora  <-- Run this in your terminal once
    
    path_to_file = r"C:/Users/navee/Downloads/archive (10)/Books_rating.csv"
    
    # 1. Get a memory-safe sample from the huge file
    sampled_df = get_review_sample_from_chunks(path_to_file, sample_size=50_000)
    
    # 2. Generate word clouds from the sample
    generate_sentiment_wordclouds(sampled_df)