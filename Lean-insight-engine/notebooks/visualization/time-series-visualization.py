# time_series_visualization.py (Self-Contained Version)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os # Good practice to include

# --- Functions copied from data_processing.py are now here ---

def clean_chunk(chunk_df):
    """
    Cleans a DataFrame chunk by dropping rows with missing essential data.
    (Assuming this is the cleaning logic you need).
    """
    chunk_df.dropna(subset=['review/time', 'review/score'], inplace=True)
    return chunk_df

# --- End of copied functions ---


def analyze_reviews_over_time(file_path, chunk_size=500_000, freq='M'):
    """
    Analyzes review volume and average score over time from a large CSV file
    using memory-efficient chunking.
    """
    print("Starting time-series analysis with chunking...")
    
    all_chunk_aggs = []

    # Use pd.read_csv directly since get_chunk_iterator is no longer needed.
    # We only load necessary columns to save memory.
    chunk_iterator = pd.read_csv(
        file_path,
        chunksize=chunk_size,
        usecols=['review/time', 'review/score'] # <-- MAJOR MEMORY OPTIMIZATION
    )

    for i, chunk in enumerate(chunk_iterator):
        print(f"Processing chunk {i+1}...")
        
        # 1. Clean data and convert time column
        chunk = clean_chunk(chunk) # Use the function we defined above
        chunk['review/time'] = pd.to_datetime(chunk['review/time'], unit='s', errors='coerce')
        chunk.dropna(subset=['review/time'], inplace=True) # Drop rows where date conversion failed
        
        if chunk.empty:
            continue

        # 2. Create the grouping key
        chunk['review_date'] = chunk['review/time'].dt.to_period(freq).dt.to_timestamp()

        # 3. Perform aggregation ON THE CHUNK
        chunk_agg = chunk.groupby('review_date').agg(
            TotalScoreSum=('review/score', 'sum'),
            TotalReviews=('review/score', 'count')
        )
        all_chunk_aggs.append(chunk_agg)

    print("All chunks processed. Combining results...")
    
    if not all_chunk_aggs:
        print("No data found to aggregate.")
        return pd.DataFrame(columns=['review_date', 'TotalReviews', 'AvgScore'])

    combined_df = pd.concat(all_chunk_aggs)
    
    # 5. Perform the FINAL aggregation
    final_time_df = combined_df.groupby(combined_df.index).sum()
    
    # 6. Calculate the true average score
    final_time_df['AvgScore'] = final_time_df['TotalScoreSum'] / final_time_df['TotalReviews']

    # 7. Clean up the final DataFrame
    final_time_df = final_time_df.drop(columns=['TotalScoreSum'])
    final_time_df = final_time_df.reset_index()

    print("Analysis complete.")
    return final_time_df.sort_values('review_date')


def plot_time_series_data(df):
    """
    Generates and displays plots for review volume and average score over time.
    """
    if df.empty:
        print("Cannot plot empty DataFrame.")
        return

    # Plot 1: Review Volume Over Time
    plt.figure(figsize=(15, 7))
    sns.lineplot(x='review_date', y='TotalReviews', data=df, color='blue', marker='o', markersize=4)
    plt.title("Review Volume Over Time", fontsize=16)
    plt.xlabel("Date")
    plt.ylabel("Number of Reviews")
    plt.xticks(rotation=45)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()

    # Plot 2: Average Score Over Time
    plt.figure(figsize=(15, 7))
    sns.lineplot(x='review_date', y='AvgScore', data=df, color='green', marker='o', markersize=4)
    plt.title("Average Book Score Over Time", fontsize=16)
    plt.xlabel("Date")
    plt.ylabel("Average Score")
    plt.ylim(3.5, 5) 
    plt.xticks(rotation=45)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Using a raw string (r"...") is best practice for Windows paths
    path_to_file = r"C:/Users/navee/Downloads/archive (10)/Books_rating.csv"
    
    time_series_df = analyze_reviews_over_time(path_to_file, freq='M')
    
    if not time_series_df.empty:
        print("\nDisplaying plots...")
        plot_time_series_data(time_series_df)