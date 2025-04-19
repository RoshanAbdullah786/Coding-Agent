import os
import re
import fnmatch
from Agents.agent_tools.utils.text_operations.response_generator import response_text
from Agents.logg.logger import logger


def regex_search(path, regex_pattern, file_pattern='*', context_lines=2):
    """
    Search files in a directory recursively for a regex pattern, showing matches with context.
    
    Parameters:
    - path (str): The directory path to search in.
    - regex_pattern (str): The regex pattern to search for.
    - file_pattern (str): Optional, glob pattern like '*.py' or '*.txt'.
    - context_lines (int): Number of context lines before and after the match.
    """
    compiled_regex = re.compile(regex_pattern)
    output = ""  # Start with an empty string

    for root, dirs, files in os.walk(path):
        for file_name in files:
            if fnmatch.fnmatch(file_name, file_pattern):
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    for i, line in enumerate(lines):
                        if compiled_regex.search(line):
                            output += f"\nFile Path: {file_path}\n"
                            output += f"Line: {i + 1}\n"
                            output += "Context:\n"
                            
                            # Calculate context start and end
                            start = max(i - context_lines, 0)
                            end = min(i + context_lines + 1, len(lines))
                            
                            for context_line in lines[start:end]:
                                output += context_line.rstrip() + "\n"
                            
                            output += "-" * 40 + "\n"
                except Exception as e:
                    output += f"Skipping file {file_path}: {e}\n"

    # After the whole search, print everything at once
    return output

def search_files(path, regex_pattern, file_pattern='*',agent=""):
    if file_pattern == None or file_pattern == "":
        file_pattern = "*"
    try:
        logger.info(f"{agent} -- The Search tool at the path {path} has been successfully executed")
        response = f"THIS IS AN AUTOMATED MESSAGE. DO NOT REPLY TO IT CONVERSATIONALLY. THE SEARCH FILES AT THE PATH {path} HAS SUCCESSFULLY EXECUTED.THIS IS THE RESULT OF THE SEARCH.\n"
        return response_text(response+regex_search(path,regex_pattern=regex_pattern,file_pattern=file_pattern))
    except Exception as e:
        logger.warning(f"{agent} -- The Search tool at the path {path} has produced the following Error when executed ==>{e}")
        return response_text(f"THIS IS AN AUTOMATED MESSAGE. DO NOT REPLY TO IT CONVERSATIONALLY. THE SEARCH FILES AT THE PATH {path} HAS PRODUCED THE FOLLOWING ERROR ==> {e} WHEN EXECUTED")
        






