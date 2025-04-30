import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from fastapi import FastAPI, File, UploadFile, HTTPException, Query, BackgroundTasks
from fastapi.responses import JSONResponse
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv() 

app = FastAPI()

API_URL = os.getenv("API_URL", "http://172.17.0.1:8000") 
API_KEY = os.getenv("API_KEY", "") 
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "./uploads/")
ALLOWED_EXTENSIONS = {"apk", "zip", "ipa", "appx"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post("/file-upload")
async def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    if not file:
        raise HTTPException(status_code=400, detail="No file part in the request")

    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Allowed file types are apk, zip, ipa, appx")

    filename = secure_filename(file.filename)
    filefullpath = os.path.join(UPLOAD_FOLDER, filename)
    
    with open(filefullpath, "wb") as f:
        content = await file.read()
        f.write(content)

    task_id = await scan_file(filename, filefullpath)
    
    
    background_tasks.add_task(task_id)

    return JSONResponse(content={"task_id": task_id}, status_code=200)

async def scan_file(filename, filefullpath):
    multipart_data = MultipartEncoder(fields={'file': (
                            filename,
                            open(filefullpath, 'rb'),
                            'application/octet-stream')})

    headers = {
        'Content-Type': multipart_data.content_type,
        'Authorization': f'Bearer {API_KEY}'  
    }

    response = requests.post(f"{API_URL}/apiv2/tasks/create/file/", headers=headers, data=multipart_data)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error while sending file to CAPEv2")

    task_id = response.json()["data"]["task_ids"][0]
    return task_id

@app.get("/ready")
async def ready(task_id: int = Query(...)):
    headers = {
        'Authorization': f'Bearer {API_KEY}'  
    }

    response = requests.get(f"{API_URL}/apiv2/tasks/get/report/{task_id}/json/", headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error while fetching report from CAPEv2")

    return JSONResponse(content=response.json(), status_code=200)
