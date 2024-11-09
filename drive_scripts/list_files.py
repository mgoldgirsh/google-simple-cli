from typing import Any, List

import utils


def list_files(service: Any, num_files: int) -> List:
    """Lists the num_files most recent number of files accessed in the google drive.

    Args:
        service (Any): the service to call to perform the list files requests
        num_files (int): the number of most recent files to get
        
    Returns:
        List: of files obtained by the drive api call
    """
    # Call the Drive v3 API
    results = (
        service.files()
        .list(pageSize=num_files, 
              supportsAllDrives=True, 
              includeItemsFromAllDrives=True, 
              fields="nextPageToken, files(id, name)", 
              orderBy="recency desc")
        .execute()
    )
    items = results.get("files", [])

    if not items:
      print("No files found.")
      return
    
    print(f"\nTop {num_files} Most Recently Opened Files/Folders:")
    column_formatted = utils.column_format(list(map(lambda i: i['name'], items)), 
                                           list(map(lambda i: i['id'], items)), 
                                           titles=("Filename", "File Id"))
    print("\n".join(column_formatted))
    
    return items