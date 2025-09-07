import os
import sys

def run_checks():
    """Run startup checks"""
    try:
        # Test basic imports
        import pandas as pd
        import numpy as np
        from sklearn.metrics.pairwise import cosine_similarity
        print("[OK] Basic packages imported")
        
        # Test data loading
        if os.path.exists("data/fashion_with_embeddings.pkl"):
            df = pd.read_pickle("data/fashion_with_embeddings.pkl")
            print(f"[OK] Dataset loaded: {len(df)} items")
        else:
            print("[ERROR] Dataset file not found: data/fashion_with_embeddings.pkl")
            return False
        
        # Test model imports
        from models.capsule import capsule_optimizer
        from models.trend_analysis import analyze_seasonal_trends
        print("[OK] Model imports successful")
        
        return True
        
    except ImportError as e:
        print(f"[ERROR] Missing package: {e}")
        print("Install with: pip install fastapi uvicorn pandas numpy scikit-learn pydantic python-multipart")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def main():
    """Main function with proper multiprocessing support"""
    print("Starting StyleGenius Backend...")
    
    if not run_checks():
        sys.exit(1)
    
    # Start the server
    print("[OK] All checks passed. Starting server...")
    print("Server will be available at: http://localhost:8000")
    print("API docs at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop")
    
    import uvicorn
    # Disable reload on Windows to avoid multiprocessing issues
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    # Required for Windows multiprocessing
    from multiprocessing import freeze_support
    freeze_support()
    main()
