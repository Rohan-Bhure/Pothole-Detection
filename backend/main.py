import os
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ai_pipeline import PotholeDetector

# 1. Initialize FastAPI application
app = FastAPI(title="Pothole Detection API", version="1.0")
print("Working")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Note: For production, replace "*" with your React app's specific URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Load the AI Pipeline into memory
# This happens only once when the server starts, preventing lag on individual requests.
# Make sure you download 'yolov8n.pt' and place it in the 'models/' folder!
print("Loading AI Models... This might take a few seconds.")
detector = PotholeDetector(yolo_model_path="models/pothole_yolov8_v2.pt")

# 4. Ensure the uploads directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def health_check():
    """Simple health check endpoint to verify the server is running."""
    return {"status": "online", "message": "Pothole Detection API is active."}

@app.post("/analyze")
async def analyze_road_image(file: UploadFile = File(...)):
    """
    Receives an image from React, processes it through YOLO + Faster R-CNN,
    and returns GPS data, pothole counts, sizes, and severity.
    """
    try:
        # Save the uploaded file temporarily
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
       
        results = detector.analyze_image(file_path)
        
       
        os.remove(file_path)

        
        return results

    except Exception as e:
        return {"status": "error", "message": str(e)}