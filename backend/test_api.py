#!/usr/bin/env python3
"""
Test script to verify StyleGenius API functionality
Run this to check if all endpoints work correctly
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path

def test_data_loading():
    """Test if data loads correctly"""
    try:
        df = pd.read_pickle("data/fashion_with_embeddings.pkl")
        print(f"[OK] Dataset loaded: {len(df)} items")
        print(f"[OK] Columns: {list(df.columns)}")
        return True
    except Exception as e:
        print(f"[ERROR] Data loading failed: {e}")
        return False

def test_imports():
    """Test if all imports work"""
    try:
        from models.capsule import capsule_optimizer, get_recommendations_with_serendipity
        from models.trend_analysis import analyze_seasonal_trends, get_trending_items
        print("[OK] All model imports successful")
        return True
    except Exception as e:
        print(f"[ERROR] Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic API functions"""
    try:
        # Test data loading in models
        from models.capsule import DF as capsule_df
        from models.trend_analysis import DF as trend_df
        
        print(f"[OK] Capsule model data: {len(capsule_df)} items")
        print(f"[OK] Trend model data: {len(trend_df)} items")
        
        # Test basic functions
        sample_ids = capsule_df['id'].head(5).tolist()
        result = capsule_optimizer(sample_ids, budget=8)
        print(f"[OK] Capsule optimizer works: {len(result['capsule_items'])} items")
        
        return True
    except Exception as e:
        print(f"[ERROR] Functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("StyleGenius API Tests")
    print("=" * 30)
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    tests = [
        ("Data Loading", test_data_loading),
        ("Imports", test_imports),
        ("Basic Functionality", test_basic_functionality)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if not test_func():
            all_passed = False
    
    print("\n" + "=" * 30)
    if all_passed:
        print("[SUCCESS] All tests passed! Your API is ready to run.")
        print("Run: python run_server.py")
    else:
        print("[FAILED] Some tests failed. Check the errors above.")

if __name__ == "__main__":
    import os
    main()
