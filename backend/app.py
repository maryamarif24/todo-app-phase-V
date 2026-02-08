import os
import sys
from pathlib import Path

# Add the backend directory to the Python path so imports work correctly
sys.path.append(str(Path(__file__).resolve().parent))

from src.main import app  # Import the FastAPI app from src/main.py

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=int(os.environ.get("PORT", 7860)),
        reload=False
    )