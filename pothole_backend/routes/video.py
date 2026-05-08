from fastapi import APIRouter, UploadFile, File
import cv2, shutil, uuid, os
from services.roboflow_service import run_model

router = APIRouter()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.post("/video-detect")
async def detect_video(file: UploadFile = File(...)):

    file_id = str(uuid.uuid4())

    input_path = f"{UPLOAD_DIR}/{file_id}.mp4"
    output_path = f"{OUTPUT_DIR}/{file_id}.mp4"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    cap = cv2.VideoCapture(input_path)

    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = int(cap.get(5))

    out = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (width, height)
    )

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % 5 == 0:
            cv2.imwrite("temp.jpg", frame)

            result = run_model("temp.jpg", "video")
            preds = result['predictions']['predictions']

            for p in preds:
                x, y, w, h = p['x'], p['y'], p['width'], p['height']

                x1 = int(x - w/2)
                y1 = int(y - h/2)
                x2 = int(x + w/2)
                y2 = int(y + h/2)

                cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,255), 2)

        out.write(frame)
        frame_count += 1

    cap.release()
    out.release()

    return {"output_video": output_path}