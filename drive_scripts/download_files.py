import io
import os
from typing import Any, List
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError


def download_file(service: Any, file_id: str) -> List:
    """Lists the num_files most recent number of files accessed in the google drive.

    Args:
        service (Any): the service to call to perform the list files requests
        file_id (str): the file_id of the file wanting to be downloaded
        
    Returns:
        List: of files obtained by the drive api call
    """
    try:
        # Call the Drive v3 API
        file_metadata = (
            service.files()
            .get(fileId=file_id)
            .execute()
        )
        filepath = file_metadata['name'] + ".pdf"
        
        request = (
            service.files()
            .export_media(fileId=file_id, mimeType='application/pdf')
        )
        f = io.BytesIO()
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
       
        with open(filepath, 'wb') as fi:
           fi.write(f.getvalue())
       
        print(f"Downloaded File: \"{os.getcwd() + os.path.sep + filepath}\"")
    except HttpError as error:
        print(f"An error occurred: {error}")
