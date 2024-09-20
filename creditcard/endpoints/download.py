from creditcard.enums import *
from creditcard.utils.download import download_html
from pydantic import BaseModel
import os

USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0'

class DownloadRequest(BaseModel):
    url: str
    file_path: str
    force_download: bool = False
    user_agent : str = USER_AGENT
    
class DownloadResponse(BaseModel):
    status_code : str
    exists: bool = False # File already exists
    file_path : str = None # Path to downloaded file
    file_overwritten : bool = False # File was overwritten

def download(request : DownloadRequest) -> DownloadResponse:
    """
    Downloads a file from the given URL and saves it to the specified file path.
    Args:
        request (DownloadRequest): The download request object containing the necessary information.
    Returns:
        DownloadResponse: The download response object containing the status code, file path, and file overwritten flag.
    """
    
    file_path = request.file_path
    exists = os.path.exists(file_path)
    file_overwritten = False
    status_code = "No Status Code"
    
    if exists and not request.force_download:
        status_code = "200"
    elif not exists or request.force_download:
        file_path, status_code = download_html(user_agent=request.user_agent,
                                               url=request.url,
                                               file_path=file_path)
        file_overwritten = exists

    return DownloadResponse(
        status_code=status_code,
        file_path=file_path,
        file_overwritten=file_overwritten)