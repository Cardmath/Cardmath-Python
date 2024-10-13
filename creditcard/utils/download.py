import requests
import os

# Overwrites existing files
def download_html(user_agent : str, url : str, file_path : str) -> str:
    headers = {
        'User-Agent': user_agent
    }
    response = requests.get(url, headers=headers, timeout=10)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    
    return file_path, str(response.status_code)

def remove_if_exists(file_path : str):
    if os.path.exists(file_path):
        os.remove(file_path)