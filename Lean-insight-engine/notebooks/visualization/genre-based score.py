# genre_based_score_analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_and_plot_genres(aggregated_file, book_data_file):
    """
    Loads pre-aggregated review data and book metadata to analyze and
    visualize average scores by genre.

    This function is fast because it works with a pre-processed summary file,
    not the raw multi-gigabyte review file.

    Parameters:
    - aggregated_file: Path to the 'aggregated_reviews.csv' file.
    - book_data_file: Path to the 'Books_data.csv' file with genre info.
    """
    print("Loading pre-processed data...")
    # 1. Load the two required files. These are small enough to fit in memory.
    try:
        aggregated_df = pd.read_csv(aggregated_file)
        books_df = pd.read_csv(book_data_file, usecols=['Title', 'categories'])
    except FileNotFoundError as e:
        print(f"Error: Could not find a required file. {e}")
        print("Please ensure both 'aggregated_reviews.csv' and 'Books_data.csv' are at the correct paths.")
        return

    print("Data loaded. Merging and analyzing genres...")

    # 2. Prepare the books data
    books_df.dropna(subset=['Title', 'categories'], inplace=True)
    books_df.drop_duplicates(subset=['Title'], inplace=True)
    
    # Extract the primary genre from the 'categories' column
    books_df['MainGenre'] = books_df['categories'].apply(
        lambda x: str(x).split(',')[0].strip("[]'\" ")
    )
    
    # 3. Merge your aggregated scores with the genre data
    # Use an 'inner' merge to only keep titles that exist in both files.
    merged_df = pd.merge(
        aggregated_df,
        books_df[['Title', 'MainGenre']],
        on='Title',
        how='inner'
    )

    # 4. Calculate the weighted average score for each genre.
    # This is more accurate than a simple average of 'AvgScore'.
    # It gives more weight to books with more reviews.
    merged_df['WeightedScoreSum'] = merged_df['AvgScore'] * merged_df['TotalReviews']
    
    genre_summary = merged_df.groupby('MainGenre').agg(
        TotalWeightedScore=('WeightedScoreSum', 'sum'),
        TotalReviews=('TotalReviews', 'sum'),
        BookCount=('Title', 'count') # Count how many unique books are in the genre
    ).reset_index()

    # Calculate the final, accurate average score for the genre
    genre_summary['FinalAvgScore'] = genre_summary['TotalWeightedScore'] / genre_summary['TotalReviews']

    # 5. Filter out genres with a small number of books for statistical significance
    min_books_per_genre = 50
    filtered_genres = genre_summary[genre_summary['BookCount'] > min_books_per_genre]

    # --- Plotting ---
    
    # Select the top 25 genres by book count for a clean plot
    top_genres_to_plot = filtered_genres.sort_values('BookCount', ascending=False).head(25)

    print("Generating plot...")
    plt.figure(figsize=(12, 10))
    sns.barplot(
        data=top_genres_to_plot.sort_values('FinalAvgScore', ascending=False),
        x='FinalAvgScore',
        y='MainGenre',
        palette='magma'
    )
    
    plt.title(f"Average Score by Genre (Genres with >{min_books_per_genre} Books)", fontsize=16)
    plt.xlabel("Weighted Average Score", fontsize=12)
    plt.ylabel("Genre", fontsize=12)
    plt.xlim(3.8, 4.5) # Zoom in to see the differences more clearly
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Define the paths based on your folder structure
    # The 'output' folder is inside the 'notebooks' folder
    aggregated_reviews_path = r'C:\Pandas\Lean-insight-engine\notebooks\output\aggregated_reviews.csv'
    
    # The raw data is likely in the 'data' folder at the root
    # Or you can use the absolute path you had before.
    book_data_path = r"C:/Users/navee/Downloads/archive (10)/Books_data.csv"

    # Run the analysis and plotting function
    analyze_and_plot_genres(aggregated_reviews_path, book_data_path)