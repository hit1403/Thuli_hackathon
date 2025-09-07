import pandas as pd
import numpy as np
from models.capsule import get_recommendations_with_serendipity

def debug_recommendations():
    """Debug the recommendations function"""
    try:
        # Test with some sample liked IDs
        liked_ids = [8810, 2880]  # Sample IDs from the dataset
        
        print("Testing recommendations with liked_ids:", liked_ids)
        result = get_recommendations_with_serendipity(liked_ids, serendipity=0.5, limit=5)
        print("SUCCESS: Got recommendations")
        print(f"Number of recommendations: {len(result['recommendations'])}")
        
    except Exception as e:
        print(f"ERROR in recommendations: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_recommendations()
