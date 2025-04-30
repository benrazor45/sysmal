import os
from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from app.config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from app.services import scan_file, get_report_json

router = APIRouter()

@router.post("/file-upload")
async def upload_file(file: UploadFile = File(...)):
    extension = file.filename.split('.')[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed.")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    try:
        task_id = scan_file(file.filename, file_path)
        return JSONResponse(content={"task_id": task_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ready")
def check_ready(task_id: int = Query(...)):
    try:
        report = get_report_json(task_id)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
