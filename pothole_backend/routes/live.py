from fastapi import APIRouter
import cv2
from services.roboflow_service import run_model

router = APIRouter()

@router.get("/live-detect")
def live_detect():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imwrite("temp.jpg", frame)

        result = run_model("temp.jpg", "live")
        preds = result['predictions']['predictions']

        for p in preds:
            x, y, w, h = p['x'], p['y'], p['width'], p['height']

            x1 = int(x - w/2)
            y1 = int(y - h/2)
            x2 = int(x + w/2)
            y2 = int(y + h/2)

            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,255), 2)

        cv2.imshow("Live Detection", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return {"message": "Live session ended"}