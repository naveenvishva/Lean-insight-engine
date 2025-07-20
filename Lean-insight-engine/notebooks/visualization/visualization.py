# visual_summary.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_aggregated_data(file_path):
    return pd.read_csv(file_path)

def plot_top_books(df, top_n=20):
    """
    Plot top N books by total number of reviews.
    """
    top_books = df.sort_values('TotalReviews', ascending=False).head(top_n)

    plt.figure(figsize=(12, 8))
    sns.barplot(data=top_books, y='Title', x='TotalReviews', palette='viridis')
    plt.title(f"Top {top_n} Most Reviewed Books", fontsize=16)
    plt.xlabel("Number of Reviews")
    plt.ylabel("Book Title")
    plt.tight_layout()
    plt.show()

def plot_score_distribution(df):
    """
    Plot distribution of average scores across books.
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(df['AvgScore'], bins=30, kde=True, color='skyblue')
    plt.title("Distribution of Average Book Scores", fontsize=16)
    plt.xlabel("Average Score")
    plt.ylabel("Number of Books")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    aggregated_path = r"C:\Pandas\Lean-insight-engine\notebooks\output\aggregated_reviews.csv"  # Assume this is saved from chunk_analysis
    df = load_aggregated_data(aggregated_path)

    plot_top_books(df, top_n=20)
    plot_score_distribution(df)


