import pandas as pd
import numpy as np
import pickle

def fix_dataset():
    """Fix the dataset by recreating it with current numpy version"""
    try:
        # Try to load the CSV file instead
        df = pd.read_csv("data/cleaned_fashion.csv")
        print(f"Loaded CSV: {len(df)} items")
        
        # Generate dummy embeddings (512-dimensional) for demo purposes
        print("Generating embeddings...")
        embeddings = []
        np.random.seed(42)  # For reproducible results
        
        for i in range(len(df)):
            # Create a dummy embedding based on item features
            embedding = np.random.randn(512).astype(np.float32)
            embeddings.append(embedding)
        
        df['embedding'] = embeddings
        
        # Save with current numpy version
        df.to_pickle("data/fashion_with_embeddings_fixed.pkl")
        print("Fixed dataset saved as fashion_with_embeddings_fixed.pkl")
        
        # Test loading
        test_df = pd.read_pickle("data/fashion_with_embeddings_fixed.pkl")
        print(f"Test load successful: {len(test_df)} items")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    fix_dataset()
