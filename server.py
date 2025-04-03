from fastapi import FastAPI,UploadFile,File
from fastapi.responses import FileResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import execute
from mcp_server.helper import Remove
import os
from mimetypes import MimeTypes
from googleapiclient.http import MediaFileUpload
from mcp_server.helper import Auth
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

class QueryHandler(BaseModel):
    query:str

@app.post("/send")
def NLP(query: QueryHandler):
    nlp_query = query.query
    res = execute(nlp_query)

    print(f"Response from execute: {res}")  # Debugging

    # Extract the result value from the dictionary
    if isinstance(res, dict) and res.get('result') == 'File downloaded successfully.':
        print("Condition matched! Returning 'download_file'.")
        return {'result': {'result':'download_file'}}

    print("Condition not matched. Calling Remove()...")
    Remove()
    return {"result": res}
    
def file_upload(filepath: str) -> str:
    """Upload a file to Google Drive."""
    try:
        service=Auth()
        if not os.path.exists(filepath):
            print("File does not exist.")
            return "Error: File not found."

        name = os.path.basename(filepath)
        mimetype = MimeTypes().guess_type(name)[0] or 'application/octet-stream'
        file_metadata = {'name': name}
        media = MediaFileUpload(filepath, mimetype=mimetype)

        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"File Uploaded: {file.get('id')}")
        return f"File uploaded successfully. ID: {file.get('id')}"
    except Exception as e:
        print(f"Error during file upload: {e}")
        return f"Error: {e}"

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    UPLOAD_FOLDER="uploads"
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())
    res=file_upload(file_location)
    return {"filename": file.filename, "content_type": file.content_type, "file_path": file_location}


DOWNLOAD_FOLDER = "download"  # Folder where the file is stored
FILE_NAME = "PM YUVA 3.pdf"  # The file to be downloaded

@app.get("/download")
async def download_file():
    file_path = os.path.join(DOWNLOAD_FOLDER, FILE_NAME)
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    
    return FileResponse(file_path, filename=FILE_NAME, media_type='application/pdf')
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8001)