from creditcard.enums import *
from creditcard.schemas import DownloadRequest, DownloadResponse
from creditcard.utils.download import download_html
import os

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