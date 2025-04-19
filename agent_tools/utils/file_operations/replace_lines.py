import os
import re
from Agents.agent_tools.utils.text_operations.response_generator import response_text
from Agents.logg.logger import logger


def replace_in_file(path, diff, agent):
    """
    Replace sections of content in an existing file using SEARCH/REPLACE blocks.
    
    Args:
        path (str): The path of the file to modify
        diff (str): One or more SEARCH/REPLACE blocks following the format:
            <<<<<<< SEARCH
            [exact content to find]
            =======
            [new content to replace with]
            >>>>>>> REPLACE
    
    Returns:
        str: A multiline string containing detailed results of all replacements
    """
    result_lines = []
    result_lines.append(f"File: {path}")
    
    # Ensure the file exists
    if not os.path.exists(path):
        result_lines.append(f"ERROR: File '{path}' does not exist.")
        return "\n".join(result_lines)
    
    # Read the entire file content
    try:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        logger.warning(f"{agent} -- Replace Tool -- ERROR: Could not read file {path} ")
        result_lines.append(f"ERROR: Could not read file '{path}': {str(e)}")
        return "\n".join(result_lines)
    
    # Parse the diff blocks
    pattern = r'<<<<<<< SEARCH\n(.*?)\n=======\n(.*?)\n>>>>>>> REPLACE'
    blocks = re.findall(pattern, diff, re.DOTALL)
    
    if not blocks:
        logger.warning(f"{agent} -- Replace Tool -- No valid SEARCH/REPLACE blocks found" )
        result_lines.append("ERROR: No valid SEARCH/REPLACE blocks found in the diff.")
        return "\n".join(result_lines)
    
    # Apply each replacement block
    modified_content = content
    successful_replacements = 0
    failed_replacements = 0
    block_index = 0
    
    for search_text, replace_text in blocks:
        block_index += 1
        block_id = f"Block #{block_index}"
        
        if search_text in modified_content:
            modified_content = modified_content.replace(search_text, replace_text, 1)
            successful_replacements += 1
            result_lines.append(f"SUCCESS: {block_id} - Replacement applied")
        else:
            failed_replacements += 1
            # Include part of the search text for easier identification (limited to 50 chars)
            preview = search_text[:50] + "..." if len(search_text) > 50 else search_text
            logger.warning(f"{agent} -- Replace Tool -- Search text not found" )
            result_lines.append(f"FAILED: {block_id} - Search text not found: {preview}")
    
    # Write back the modified content if any replacements were made
    if successful_replacements > 0:
        try:
            with open(path, 'w', encoding='utf-8') as file:
                file.write(modified_content)
            result_lines.append(f"File saved with {successful_replacements} successful replacements")
        except Exception as e:
            result_lines.append(f"ERROR: Could not write to file '{path}': {str(e)}")
            result_lines.append("Warning: Changes were not saved")
    else:
        result_lines.append("No replacements were made. File remains unchanged.")
    
    # Summary statistics
    result_lines.append(f"\nSUMMARY:")
    result_lines.append(f"Total blocks: {len(blocks)}")
    result_lines.append(f"Successful: {successful_replacements}")
    result_lines.append(f"Failed: {failed_replacements}")
    
    return "\n".join(result_lines)

def search_and_replace(path,diff,agent):
    logger.info(f"{agent} -- The Replace tool at the path {path} has been successfully executed")
    response = f"THIS IS AN AUTOMATED MESSAGE. DO NOT REPLY TO IT CONVERSATIONALLY. THE REPLACE IN FILE AT THE PATH {path} HAS SUCCESSFULLY EXECUTED.THE RESULT IS GIVEN BELOW"
    return response_text(response+replace_in_file(path,diff,agent))