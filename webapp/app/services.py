import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from app.config import API_URL, API_KEY

def scan_file(filename: str, file_path: str) -> int:
    multipart_data = MultipartEncoder(fields={
        'file': (filename, open(file_path, 'rb'), 'application/octet-stream')
    })

    headers = {
        'Content-Type': multipart_data.content_type,
        'Authorization': API_KEY
    }

    response = requests.post(f"{API_URL}/apiv2/tasks/create/file/", headers=headers, data=multipart_data)
    response.raise_for_status()
    task_id = response.json()["data"]["task_ids"][0]
    return task_id

def get_report_json(task_id: int) -> dict:
    headers = {'Authorization': API_KEY}
    response = requests.get(f"{API_URL}/apiv2/tasks/get/report/{task_id}/json/", headers=headers)
    response.raise_for_status()
    return response.json()
