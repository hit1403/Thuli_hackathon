import requests
import json

def test_api_endpoints():
    """Test all API endpoints to ensure they work correctly"""
    base_url = "http://localhost:8000"
    
    print("Testing StyleGenius API endpoints...")
    
    # Test 1: Get quiz items
    print("\n1. Testing /quiz/items")
    try:
        response = requests.get(f"{base_url}/quiz/items")
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Got {len(data['items'])} items")
            print(f"  Sample item: {data['items'][0]['productDisplayName']}")
            quiz_items = data['items']
        else:
            print(f"FAILED: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"ERROR: {e}")
        return
    
    # Test 2: Submit quiz feedback
    print("\n2. Testing /quiz/feedback")
    try:
        feedback_data = [
            {"item_id": quiz_items[0]['id'], "liked": True},
            {"item_id": quiz_items[1]['id'], "liked": False},
            {"item_id": quiz_items[2]['id'], "liked": True}
        ]
        
        response = requests.post(
            f"{base_url}/quiz/feedback",
            json=feedback_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Profile created with {data['profile']['liked_count']} liked items")
            print(f"  Style personality: {data['profile']['style_personality']}")
            liked_ids = data['liked_ids']
        else:
            print(f"FAILED: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"ERROR: {e}")
        return
    
    # Test 3: Get recommendations
    print("\n3. Testing /recommendations")
    try:
        rec_data = {
            "liked_ids": liked_ids,
            "serendipity": 0.5,
            "limit": 10
        }
        
        response = requests.post(
            f"{base_url}/recommendations",
            json=rec_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Got {len(data['recommendations'])} recommendations")
            print(f"  Top recommendation: {data['recommendations'][0]['item']['productDisplayName']}")
        else:
            print(f"FAILED: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"ERROR: {e}")
        return
    
    # Test 4: Get capsule wardrobe
    print("\n4. Testing /capsule")
    try:
        capsule_data = {
            "liked_ids": liked_ids,
            "budget": 8,
            "alpha": 0.6,
            "beta": 0.3,
            "gamma": 0.1
        }
        
        response = requests.post(
            f"{base_url}/capsule",
            json=capsule_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Generated capsule with {len(data['capsule_items'])} items")
            print(f"  Outfits possible: {data['outfits_possible']}")
            print(f"  Categories covered: {data['optimization_stats']['categories_covered']}")
        else:
            print(f"FAILED: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"ERROR: {e}")
        return
    
    # Test 5: Get item details
    print("\n5. Testing /item/{item_id}")
    try:
        item_id = quiz_items[0]['id']
        response = requests.get(f"{base_url}/item/{item_id}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Got details for item {item_id}")
            print(f"  Product: {data['productDisplayName']}")
        else:
            print(f"FAILED: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"ERROR: {e}")
        return
    
    print("\nAll API endpoints are working correctly!")
    print("Your StyleGenius backend is ready for the React Native frontend!")

if __name__ == "__main__":
    test_api_endpoints()
