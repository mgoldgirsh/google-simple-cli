import io
import os
from pathlib import Path
from typing import Any, List
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

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
        file_metadata = {"name": Path(filename).name}
        
        file = (
            service.files()
            .create(body=file_metadata, 
                    media_body=MediaFileUpload(Path(filename).name, mimetype=utils.ext_to_mime(Path(filename).suffix)),
                    fields='id')
            .execute()
        )
       
        print(f"Uploaded File: \"{filename}\" with file_id: \"{file.get('id')}\" into drive!")
    except HttpError as error:
        print(f"An error occurred: {error}")
