import requests
import os
from Agents.agent_tools.config.config_read import load_config
from Agents.agent_tools.utils.text_operations.response_generator import response_text
from Agents.logg.logger import logger


def download_unsplash_image(file_path: str,keyword: str,orient) -> str:
    # Replace YOUR_ACCESS_KEY with your actual Unsplash Access Key
    ACCESS_KEY = load_config()["unsplash_api_key"]
    url = "https://api.unsplash.com/photos/random"
    headers = {
        "Accept-Version": "v1",
        "Authorization": f"Client-ID {ACCESS_KEY}"
    }
    params = {
        "query": keyword,
        "orientation": orient  # Optional: you can remove or change to 'portrait', 'squarish'
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    # Get the URL of the image (full quality)
    image_url = data['urls']['full']

    # Download the image
    image_response = requests.get(image_url)
    image_response.raise_for_status()

    # Save the image to the given path
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as file:
        file.write(image_response.content)
    


def placeholder_image(path,keywords,orient,agent):
    try:
        download_unsplash_image(path,keywords,orient)
        logger.info(f"{agent} -- The Download Placeholder Image tool at the path {path} has been successfully executed")
        return response_text(f"THIS IS AN AUTOMATED MESSAGE. DO NOT REPLY TO IT CONVERSATIONALLY. THE DOWNLOAD PLACEHODER IMAGE AT THE PATH {path} HAS SUCCESSFULLY EXECUTED.")
    except Exception as e:
        logger.warning(f"{agent} -- The Download Placeholder Image tool at the path {path} has produced the following Error when executed ==> {e}")
        return response_text(f"THIS IS AN AUTOMATED MESSAGE. DO NOT REPLY TO IT CONVERSATIONALLY. THE DOWNLOAD PLACEHODER IMAGE AT THE PATH {path} HAS PRODUCED THE FOLLOWING ERROR ==> {e} WHEN EXECUTED")
