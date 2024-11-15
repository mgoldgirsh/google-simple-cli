from typing import Any, List, Optional, Union

import utils
from drive_scripts import list_files

def search_files(service: Any, must_contains: Optional[Union[List[str], str]] = None, printf: bool = True) -> List:
    """Lists and searches through files that contain the must_contains in the google drive.

    Args:
        service (Any): the service to call to perform the list files requests
        must_contains: (Optional[Union[List[str], str]]): the partial filename to search for
        printf (bool): if printf true print to stdout, else do not. Default to True
        
    Returns:
        List: of files/folders obtained by the drive api call
    """
    
    if must_contains is None or len(must_contains) == 0:
        return list_files.list_files(service, 10)
    
    if isinstance(must_contains, str):
        file_name_contains = must_contains.strip().split(' ')
    elif isinstance(must_contains, list):
        file_name_contains = []
        for s in must_contains:
            s_list = s.strip().split(' ')
            file_name_contains += s_list
    else:
        if printf:
            print('Invalid arguments supplied')
        return 
    
    query = ' and '.join([f"name contains '{contain}'" for contain in file_name_contains])
    # Call the Drive v3 API
    results = (
        service.files()
        .list(q=query,
              supportsAllDrives=True, 
              includeItemsFromAllDrives=True, 
              fields="nextPageToken, files(id, name)"
              )
        .execute()
    )
    items = results.get("files", [])

    if not items:
      if printf:
        print("No files found.")
      return
    
    if printf:
      print(f"\nFiles/Folders that contain: {' '.join(file_name_contains)}")
    column_formatted = utils.column_format(list(map(lambda i: i['name'], items)), 
                                           list(map(lambda i: i['id'], items)), 
                                           titles=("Filename", "File Id"))
    if printf:
      print("\n".join(column_formatted))
    
    return items