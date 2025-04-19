import os
from Agents.agent_tools.utils.text_operations.response_generator import response_text
from Agents.logg.logger import logger

def write_to_file(path,content,agent):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w',encoding='utf-8') as file:
            file.write(content)
        logger.info(f"{agent} -- The Write to File tool at the path {path} has been successfully executed")
        return response_text(f"THIS IS AN AUTOMATED MESSAGE. DO NOT REPLY TO IT CONVERSATIONALLY. THE WRITE TO FILE AT THE PATH {path} HAS SUCCESSFULLY EXECUTED.")
    except Exception as e:
        logger.warning(f"{agent} -- The Write to File tool at the path {path} has produced the following Error when executed ==> {e}")
        return response_text(f"THIS IS AN AUTOMATED MESSAGE. DO NOT REPLY TO IT CONVERSATIONALLY. THE WRITE TO FILE AT THE PATH {path} HAS PRODUCED THE FOLLOWING ERROR ==> {e} WHEN EXECUTED")




        