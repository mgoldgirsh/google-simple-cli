import io
import os
from typing import Any, List
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

from drive_scripts import search_files
import utils

def download_file(service: Any, file_descriptor: str) -> List:
    """Lists the num_files most recent number of files accessed in the google drive.

    Args:
        service (Any): the service to call to perform the list files requests
        file_descriptor (str): the file_id/filename of the file wanting to be downloaded
        
    Returns:
        List: of files obtained by the drive api call
    """
    try:
        # try to find the file with the file_descriptor
        match = search_files.search_files(service, file_descriptor, printf=False)
        
        if match is not None and len(match) > 0:
            # the file_descriptor is a partial / full match of the file name
            # therefore use the file id for that files
            file_id = match[0]['id']
        else:
            # then the file_id is the file descriptor 
            file_id = file_descriptor        
            
        file_metadata = (
            service.files()
            .get(fileId=file_id)
            .execute()
        )
        
        formatted_mime, ext = utils.mime_to_format(file_metadata['mimeType'])
        # Tried to download a folder
        if (ext == -1):
            print(formatted_mime)
            return
        
        f = io.BytesIO()
        if (ext is not None):
            # then we need to export the file 
            filepath = file_metadata['name'] + ext
        
            request = (
                service.files()
                .export_media(fileId=file_id, mimeType=formatted_mime)
            )
        else:
            # we need to download the bytes without exporting 
            filepath = file_metadata['name']
            
            request = (
                service.files()
                .get_media(fileId=file_id)
            )
        
        # download the file
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
    
        with open(filepath, 'wb') as fi:
            fi.write(f.getvalue())
    
        print(f"Downloaded File: \"{os.getcwd() + os.path.sep + filepath}\"")
    except HttpError as error:
        print(f"An error occurred: {error}")
