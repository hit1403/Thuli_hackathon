import json
from models.capsule import get_recommendations_with_serendipity

def test_recommendations_serialization():
    """Test if recommendations can be serialized to JSON"""
    try:
        # Test with sample liked IDs
        liked_ids = [8810, 2880]
        
        print("Getting recommendations...")
        result = get_recommendations_with_serendipity(liked_ids, serendipity=0.5, limit=3)
        
        print("Testing JSON serialization...")
        json_str = json.dumps(result, indent=2)
        print("SUCCESS: JSON serialization works")
        
        # Print first recommendation to check structure
        if result['recommendations']:
            first_rec = result['recommendations'][0]
            print(f"First recommendation keys: {list(first_rec.keys())}")
            print(f"Item keys: {list(first_rec['item'].keys())}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_recommendations_serialization()
