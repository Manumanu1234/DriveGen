from helper import Auth
def file_listing(filename):
    """List all files in Google Drive (limited to 5 files)."""
    try:
        service=Auth()
        result = service.files().list(pageSize=5, fields="files(id, name)").execute()
        file_list = result.get('files', [])
        
        if not file_list:
            print("No files found.")
            return []
        ID=""
        for file in file_list:
            if file['name']==filename:
                print("Found")
                ID=""+file['id']
                break
        return ID
    except Exception as e:
        print(f"Error listing files: {e}")
        return f"Error: {e}"
