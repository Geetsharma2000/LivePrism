from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
import base64

app = FastAPI()

# Simple endpoint to check server is running
@app.get("/")
def read_root():
    return {"message": "Segmentation API is running 🚀"}

# Segmentation endpoint: accepts image and returns mask
@app.post("/segment")
async def segment_image(file: UploadFile = File(...)):
    # Read uploaded file into numpy array
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert to grayscale + threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

    # Encode mask back to base64 for return
    _, buffer = cv2.imencode(".png", mask)
    mask_base64 = base64.b64encode(buffer).decode("utf-8")

    return {"mask": mask_base64}
