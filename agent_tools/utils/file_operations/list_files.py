from Agents.agent_tools.utils.text_operations.response_generator import response_text
from Agents.logg.logger import logger

def list_files_in_the_dir(path,recursive=False):
    from pathlib import Path

    path = Path(path)
    if not path.exists() or not path.is_dir():
        raise NotADirectoryError(f"No directory found at: {path}")

    if recursive:
        files = [str(file.relative_to(path)) for file in path.rglob('*')]
    else:
        files = [str(file.name) for file in path.iterdir()]

    return "\n".join(files)


def list_files(path, recursive=False,agent=""):
    try:
        logger.info(f"{agent} -- The List Files tool at the path {path} has been successfully executed")
        return response_text(f"THIS IS AN AUTOMATED MESSAGE. DO NOT REPLY TO IT CONVERSATIONALLY. THE LIST FILES AT THE PATH {path} HAS SUCCESSFULLY EXECUTED.THIS IS THE RESULT.\n"+list_files_in_the_dir(path,recursive))
    except Exception as e:
        logger.info(f"{agent} -- The List Files tool at the path {path} has produced the follwoing error ==> {e}")
        return response_text(f"THIS IS AN AUTOMATED MESSAGE. DO NOT REPLY TO IT CONVERSATIONALLY. THE LIST FILES AT THE PATH {path} HAS PRODUCED THE FOLLOWING ERROR {e} WHEN EXECUTED")
