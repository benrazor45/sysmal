from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import handle_file_analysis
import os

router = APIRouter()

UPLOAD_DIR = "saved_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", summary="Upload malware file for analysis")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="File tidak valid")

    saved_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(saved_path, "wb") as f:
        content = await file.read()
        f.write(content)

    result = handle_file_analysis(saved_path)

    return {"status": "success", "filename": file.filename, "result": result}
