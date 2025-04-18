import io
import os
import zipfile
from tqdm import tqdm
from pathlib import Path
from typing import Any
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

from drive_scripts import search_files
import utils

def download_file(service: Any, file_descriptor: str) -> None:
    """Downloads a file or folder from google drive.

    Args:
        service (Any): the service to call to perform the list files requests
        file_descriptor (str): the file_id/filename of the file/folder wanting to be downloaded
        
    Returns:
        None: downloads the file/folder to local device
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
        
        if utils.is_folder(file_metadata['mimeType']):
            return download_folder(service, file_id, file_metadata['name'])
        
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


def download_folder(service: Any, folder_id: str, folder_name: str) -> None:
    """Downloads a specified folder as zip file without recursing through folders inside it. 

    Args:
        service (Any): the service to call to perform the download folder request
        folder_id (str): the file_id of the folder wanting to be downloaded
        folder_name (str): the name of the folder downloaded
        
    Returns:
        None: downloads the folder as zip to local device
    """
    try:
        
        files_in_folder = (
            service.files()
            .list(
                q=f'"{folder_id}" in parents',
                fields="nextPageToken, files(id, name, mimeType)"
            )
            .execute()
        )
        
        if files_in_folder is None or len(files_in_folder['files']) == 0: 
            print("No files in folder to download")
            return
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED, False) as zip_file:
            for file_metadata in tqdm(files_in_folder['files'], desc='Files in Folder'):
                # if there is a folder inside another folder then skip downloading it 
                if (utils.is_folder(file_metadata['mimeType'])):
                    continue
                
                # otherwise download the file
                formatted_mime, ext = utils.mime_to_format(file_metadata['mimeType'])
                # Tried to download a folder
                if (ext == -1):
                    print(formatted_mime)
                    return
                
                if (ext is not None):
                    # then we need to export the file 
                    filepath = file_metadata['name'] + ext
                
                    request = (
                        service.files()
                        .export_media(fileId=file_metadata['id'], mimeType=formatted_mime)
                    )
                else:
                    # we need to download the bytes without exporting 
                    filepath = file_metadata['name']
                    
                    request = (
                        service.files()
                        .get_media(fileId=file_metadata['id'])
                    )
            
                # download the file
                f = io.BytesIO()
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
            
                zip_file.writestr(folder_name+os.path.sep+Path(filepath).name, f.getvalue())
        
        # now write the zip
        with open(folder_name + ".zip", 'wb') as z:
            z.write(zip_buffer.getvalue())
        
        print(f"Downloaded Folder: \"{os.getcwd() + os.path.sep + folder_name}.zip\"")
    except HttpError as error:
        print(f"An error occurred: {error}")
