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
        ".zip":'application/zip'
    }
    return mapping[ext]
    