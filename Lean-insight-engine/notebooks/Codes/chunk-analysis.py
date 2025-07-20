# chunk_analysis.py (Refactored & Recommended)

from data_processing import get_chunk_iterator, clean_chunk
import pandas as pd
import os

def analyze_reviews_efficient(file_path, chunk_size=100_000):
    """
    Aggregates total reviews and average score per title using an efficient,
    Pandas-idiomatic approach.

    Parameters:
    - file_path: str - Path to the CSV file
    - chunk_size: int - Rows to read per chunk

    Returns:
    - pd.DataFrame with Title, TotalReviews, and AvgScore
    """
    total_counts = pd.Series(dtype=int)
    total_sums = pd.Series(dtype=float)

    for chunk in get_chunk_iterator(file_path, chunk_size):
        chunk = clean_chunk(chunk)
        
        # Group by title and get the count and sum of scores for the chunk
        chunk_agg = chunk.groupby('Title')['review/score'].agg(['count', 'sum'])
        
        # Add the chunk's aggregates to the running totals
        total_counts = total_counts.add(chunk_agg['count'], fill_value=0)
        total_sums = total_sums.add(chunk_agg['sum'], fill_value=0)

    # Combine the final series into a DataFrame
    results_df = pd.DataFrame({
        'TotalReviews': total_counts,
        'TotalScoreSum': total_sums
    })
    
    # Calculate the final average score
    results_df['AvgScore'] = results_df['TotalScoreSum'] / results_df['TotalReviews']
    
    # Clean up the DataFrame
    results_df = results_df.drop(columns=['TotalScoreSum']) # Drop intermediate column
    results_df = results_df.reset_index().rename(columns={'index': 'Title'}) # Make 'Title' a column

    return results_df.sort_values('TotalReviews', ascending=False)

if __name__ == "__main__":
    path_to_file = "C:/Users/navee/Downloads/archive (10)/Books_rating.csv"
    output_path = "output/aggregated_reviews.csv"

    print("Starting analysis...")
    final_df = analyze_reviews_efficient(path_to_file) # Using the efficient version
    print("Analysis complete.")

    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True) # exist_ok=True is a cleaner way

    # Save the DataFrame to a CSV file
    final_df.to_csv(output_path, index=False)
    
    print(f"Aggregated data saved to: {output_path}")

    # You can still print the head to see the result in the console
    print("\nTop 5 results:")
    print(final_df.head())