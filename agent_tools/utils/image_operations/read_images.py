import os
import base64
from Agents.agent_tools.utils.text_operations.response_generator import response_text_and_image,response_text
from Agents.logg.logger import logger

def get_image_name_and_base64(file_path):
    """
    Given a path to an image file, returns:
    1. The image file name
    2. The base64 encoded string with MIME type prefix
    
    Supported formats: PNG, JPEG, WEBP
    """
    # Get file name
    file_name = os.path.basename(file_path)
    
    # Determine MIME type based on extension
    extension = file_name.lower().split('.')[-1]
    if extension == 'png':
        mime_type = 'image/png'
    elif extension in ('jpg', 'jpeg'):
        mime_type = 'image/jpeg'
    elif extension == 'webp':
        mime_type = 'image/webp'
    else:
        raise ValueError(f"Unsupported file type: {extension}")
    
    # Read and encode the image
    with open(file_path, 'rb') as img_file:
        base64_string = base64.b64encode(img_file.read()).decode('utf-8')
    
    # Format it like 'data:image/jpeg;base64,...'
    data_url = f"data:{mime_type};base64,{base64_string}"
    
    return response_text_and_image(f"The follwing image is in the path {file_path}",data_url)

def read_image(paths,agent):
    response = []
    response += response_text("THIS IS AN AUTOMATED MESSAGE. DO NOT REPLY TO IT CONVERSATIONALLY.THE READ IMAGE TOOL HAS PRODUCED THE FOLLOWING RESULT.")
    if type(paths) == list:
        for image_path in paths:
            try:
                response += get_image_name_and_base64(image_path)
                logger.info(f"{agent} -- The Read Image tool has been successfully executed")
            except Exception as e:
                response += response_text(f"THIS IS AN AUTOMATED MESSAGE. DO NOT REPLY TO IT CONVERSATIONALLY.THE READ IMAGE TOOL AT THE {image_path} HAS PRODUCED THE FOLLOWING ERROR ==> {e}.")
                logger.warning(f"{agent} -- The Read Image tool has produced the follwoing error == {e}")
    return response

