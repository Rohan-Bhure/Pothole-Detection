from fastapi import APIRouter, UploadFile, File, Form
import shutil, uuid, os
from services.roboflow_service import run_model
from services.detector import draw_boxes

router = APIRouter()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.post("/detect-image")
async def detect_image(
    file: UploadFile = File(...),
    name: str = Form(...),
    phone: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...)
):
    file_id = str(uuid.uuid4())

    input_path = f"{UPLOAD_DIR}/{file_id}.jpg"
    output_path = f"{OUTPUT_DIR}/{file_id}.jpg"

    # Save image
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run detection
    result = run_model(input_path, "image")

    preds = result['predictions']['predictions']
    count = result['count_objects']

    # Draw boxes
    draw_boxes(input_path, preds, output_path)

    return {
        "status": "detected",
        "report_id": file_id,   # important for next step
        "user": {
            "name": name,
            "phone": phone,
            "location": {
                "latitude": latitude,
                "longitude": longitude
            }
        },
        "analysis": {
            "potholes_detected": count,
            "severity": "LOW" if count < 3 else "MEDIUM" if count < 7 else "HIGH"
        },
        "output_image": output_path,
        "message": f"{count} potholes detected. Please verify."
    }