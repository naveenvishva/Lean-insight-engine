# data_processing.py

import pandas as pd

def get_chunk_iterator(file_path, chunk_size=100_000):
    """
    Returns a generator that yields chunks of the dataset.

    Parameters:
    - file_path: str - Path to the CSV file
    - chunk_size: int - Number of rows per chunk

    Returns:
    - generator yielding DataFrame chunks
    """
    return pd.read_csv(
        file_path,
        chunksize=chunk_size,
        dtype={
            'Title': 'string',
            'review/score': 'float32'
        }
    )

def clean_chunk(chunk):
    """
    Perform basic cleaning operations on a chunk (if needed).
    Currently a placeholder – ready to scale for future enhancements.

    Parameters:
    - chunk: pd.DataFrame

    Returns:
    - pd.DataFrame (cleaned chunk)
    """
    # Example: Drop rows with missing score or title
    return chunk.dropna(subset=['Title', 'review/score'])
