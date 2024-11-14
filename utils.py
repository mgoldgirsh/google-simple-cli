from typing import Iterable, List, Tuple

def column_format(s1: Iterable[str], s2: Iterable[str], titles: Tuple[str, str] = None) -> List[str]:
    """Returns a formatted string so that a nice column format is maintained
       when outputting text.

    Args:
        s1 (Iterable[str]): a list of strings that are in the first column
        s2 (Iterable[str]): a list of strings that are in the second column
        titles (Tuple[str]): a tuple of titles for the first,second column. Default to None

    Returns:
        List[str]: the formatted set of strings s1   s2 that have the same spacing for column format
    """
    max_s_l = max(map(len, s1)) 
    results = []
    if titles:
        d_space = max_s_l - len(titles[0])
        results.append(f'\t{titles[0]}{" " * d_space}\t{titles[1]}')
    
    for str1, str2 in zip(s1, s2):
        d_space = max_s_l - len(str1)
        results.append(f'\t{str1}{" " * d_space}\t{str2}')
    results.append('\n')
    return results


def mime_to_format(mime: str) -> Tuple[str, str]:
    """Converts a mimeType of google drive format into the corresponding extention and corrected
    mimetype for that document. 

    Args:
        mime (str): the mimeType of the associated file

    Returns:
        str, str: corrected mimeType for that document and associated extention with it.
    """
    if ("spreadsheet" in mime):
        return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".xlsx"
    elif ("document" in mime): 
        return "application/vnd.openxmlformats-officedocument.wordprocessingml.document", ".docx"
    elif ("presentation" in mime):
        return "application/vnd.openxmlformats-officedocument.presentationml.presentation", ".pptx"
    elif ("json" in mime):
        return "application/vnd.google-apps.script+json", ".json"
    elif ("vid" in mime):
        return "application/vnd.google-apps.vid", ".mp4"
    elif ("folder" in mime):
        # TODO not supported yet
        return "Downloading folders is not supported yet...", -1
    else:
        return None, None
    

def ext_to_mime(ext: str) -> str:
    """Convert an ext (.***) to a mime type of the same kind.

    Args:
        ext (str): the extention to convert of the file

    Returns:
        str: the mime type corresponding with that file
    """
    mapping = {
        ".txt": 'text/plain',
        ".png":'image/png', 
        ".jpeg":'image/jpeg',
        ".pdf":'application/pdf',
        ".zip":'application/zip',
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".mp4": "application/vnd.google-apps.vid",
        ".json": "application/vnd.google-apps.script+json",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".ipynb": "application/vnd.google.colaboratory"   
    }
    return mapping[ext]
    