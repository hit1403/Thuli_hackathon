import pandas as pd
import numpy as np
import json

def test_quiz_endpoint_logic():
    """Test the exact logic from the quiz endpoint"""
    
    # Load dataset
    DF = pd.read_pickle("data/fashion_clean.pkl")
    print(f"Dataset loaded: {DF.shape}")
    
    # Simulate the quiz endpoint logic
    count = 20
    sample_items = []
    categories = DF['subCategory'].unique()
    
    items_per_category = max(1, count // len(categories))
    
    for category in categories:
        category_items = DF[DF['subCategory'] == category].sample(
            min(items_per_category, len(DF[DF['subCategory'] == category])),
            random_state=42
        )
        sample_items.append(category_items)
    
    # If we need more items, sample randomly
    if len(pd.concat(sample_items)) < count:
        remaining = count - len(pd.concat(sample_items))
        additional = DF.sample(remaining, random_state=42)
        sample_items.append(additional)
    
    # Concatenate and remove embedding before drop_duplicates to avoid hashing issues
    result_df = pd.concat(sample_items)
    result_df = result_df.drop(columns=['embedding'], errors='ignore').drop_duplicates().head(count)
    
    print(f"Result shape: {result_df.shape}")
    print(f"Columns: {result_df.columns.tolist()}")
    
    # Test conversion (embedding already removed)
    items_dict = result_df.to_dict(orient="records")
    
    print("Conversion successful!")
    print(f"First item keys: {list(items_dict[0].keys())}")
    
    # Test JSON serialization
    json_str = json.dumps(items_dict[0], indent=2)
    print("JSON serialization successful!")
    
    return {
        "items": items_dict,
        "total": len(result_df)
    }

if __name__ == "__main__":
    import random
    result = test_quiz_endpoint_logic()
    print(f"Final result has {len(result['items'])} items")
