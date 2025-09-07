"""
Simple server runner without reload - avoids Windows multiprocessing issues
"""
import uvicorn

if __name__ == "__main__":
    print("Starting StyleGenius Backend (Simple Mode)...")
    print("Server: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("Press Ctrl+C to stop")
    
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=False,  # Disable reload to avoid multiprocessing issues
        log_level="info"
    )
