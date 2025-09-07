import pandas as pd
import numpy as np
import json

def create_clean_dataset():
    """Create a clean dataset without numpy serialization issues"""
    
    # Load the CSV file
    df = pd.read_csv("data/cleaned_fashion.csv")
    
    # Create mock embeddings (512-dimensional vectors) that are JSON serializable
    np.random.seed(42)  # For reproducibility
    
    # Convert all data to JSON-serializable types
    clean_data = []
    
    for idx, row in df.iterrows():
        # Create a mock embedding as a regular Python list
        embedding = np.random.normal(0, 1, 512).tolist()  # Convert to list immediately
        
        item = {
            'id': int(row['id']),
            'gender': str(row['gender']) if pd.notna(row['gender']) else None,
            'masterCategory': str(row['masterCategory']) if pd.notna(row['masterCategory']) else None,
            'subCategory': str(row['subCategory']) if pd.notna(row['subCategory']) else None,
            'articleType': str(row['articleType']) if pd.notna(row['articleType']) else None,
            'baseColour': str(row['baseColour']) if pd.notna(row['baseColour']) else None,
            'season': str(row['season']) if pd.notna(row['season']) else None,
            'year': float(row['year']) if pd.notna(row['year']) else None,
            'usage': str(row['usage']) if pd.notna(row['usage']) else None,
            'productDisplayName': str(row['productDisplayName']) if pd.notna(row['productDisplayName']) else None,
            'embedding': embedding  # This is now a regular Python list
        }
        clean_data.append(item)
    
    # Create DataFrame from clean data
    clean_df = pd.DataFrame(clean_data)
    
    # Save as pickle with protocol 4 for better compatibility
    clean_df.to_pickle("data/fashion_clean.pkl", protocol=4)
    
    # Also save as JSON for debugging
    with open("data/fashion_sample.json", "w") as f:
        json.dump(clean_data[:5], f, indent=2)
    
    print(f"Created clean dataset with {len(clean_data)} items")
    print(f"Saved to data/fashion_clean.pkl")
    print(f"Sample saved to data/fashion_sample.json")
    
    return clean_df

if __name__ == "__main__":
    create_clean_dataset()
