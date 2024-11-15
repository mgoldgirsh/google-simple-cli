from pathlib import Path
from typing import Any, List
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from drive_scripts import search_files
import utils

def upload_file(service: Any, filename: str) -> List:
    """Upload a file with a specified filename into the drive

    Args:
        service (Any): the service to call to perform the list files requests
        filename (str): the filename to upload into the drive
        
    Returns:
        List: of files obtained by the drive api call
    """ 
    try:
        # Call the Drive v3 API
        
        # search for files with that filename
        match = search_files.search_files(service, Path(filename).name, printf=False)

        # if there is no match for that file upload a new file
        if (match is None or len(match) == 0):
            # upload a new file
            file_metadata = {"name": Path(filename).name}
            file = (
                service.files()
                .create(body=file_metadata, 
                        media_body=MediaFileUpload(Path(filename).name, mimetype=utils.ext_to_mime(Path(filename).suffix)),
                        fields='id')
                .execute()
        )
            print(f"Uploaded File: \"{filename}\" with file_id: \"{file.get('id')}\" into drive!")
        else:
            formatted_mimeType = utils.ext_to_mime(Path(filename).suffix)
            # otherwise update the file with a new revision 
            file = (
                service.files()
                .update(fileId=match[0]['id'],
                        body={}, 
                        media_body=MediaFileUpload(Path(filename).name, mimetype=formatted_mimeType, resumable=True),
                        fields='id')
                .execute()
            )
        print(f"Updated File: \"{filename}\" with file_id: \"{file.get('id')}\" into drive!")
        
       
    except HttpError as error:
        print(f"An error occurred: {error}")
