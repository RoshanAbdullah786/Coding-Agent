from Agents.agent_tools.utils.text_operations.response_generator import response_text
from Agents.logg.logger import logger
def ask_question_to_designer(prompt):  
    logger.info("Coding Agent -- Talking to -- Designer Agent")
    logger.debug(f"Coding Agent -- Asking ==> {prompt}")
    print(prompt)
    response = input("Enter your prompt for the coder:")
    logger.info("Coding Agent -- Finished Talking to -- Designer Agent")
    logger.debug(f"Designer Agent -- Replied ==> {response}")
    
    return response_text(response)