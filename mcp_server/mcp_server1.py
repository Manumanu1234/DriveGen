from mcp.server.fastmcp import FastMCP
import os
import io
import shutil
from mimetypes import MimeTypes
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import Resource
from helper import Auth
from helper_fun import file_listing
# Initialize FastMCP instance
mcp = FastMCP("Drive")

@mcp.tool()
def file_download(file_name: str) -> str:
    """Download files from Google Drive."""
    try:
        service=Auth()
        file_id=file_listing(file_name)
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while not done:
            status, done = downloader.next_chunk()
            print(f"Download Progress: {int(status.progress() * 100)}%")

        fh.seek(0)
        destination_dir = "./download"
        os.makedirs(destination_dir, exist_ok=True)
        destination_path = os.path.join(destination_dir, file_name)

        with open(destination_path, 'wb') as f:
            shutil.copyfileobj(fh, f)

        print("File Downloaded Successfully")
        return "File downloaded successfully."
    except Exception as e:
        print(f"Error during file download: {e}")
        return f"Error: {e}"

@mcp.tool()
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

if __name__ == "__main__":
    mcp.run(transport="stdio")