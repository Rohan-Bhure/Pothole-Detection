from fastapi import FastAPI
from routes import image, video, live, verify

app = FastAPI(title="Pothole Detection API")

app.include_router(image.router, prefix="/api")
app.include_router(video.router, prefix="/api")
app.include_router(live.router, prefix="/api")
app.include_router(verify.router, prefix="/api")
@app.get("/")
def root():
    return {"message": "Pothole Detection Backend Running"}