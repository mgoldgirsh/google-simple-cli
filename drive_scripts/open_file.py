from typing import Any, List, Optional, Union, Dict
import webbrowser

from drive_scripts import list_files

def open_file(service: Any, must_contains: Optional[Union[List[str], str]] = None) -> Dict:
    """Searches through files that contain the must_contains in the google drive and opens the first 
    link of that search.

    Args:
        service (Any): the service to call to perform the list files requests
        must_contains: (Optional[Union[List[str], str]]): the partial filename to search for
        
    Returns:
        Dict: the first file repesentation that has must_contains in it.
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
              fields="nextPageToken, files(id, name, webViewLink)"
              )
        .execute()
    )
    items = results.get("files", [])

    if not items:
        print("No files found.")
        return
    
    # open the first resulting file in a webbrowser
    webbrowser.open(items[0]['webViewLink'])
    
    return items[0]