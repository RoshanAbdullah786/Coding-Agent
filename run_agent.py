
from Agents.agent_tools.core.function.response_parser import parse
from Agents.agent_tools.core.function.tool_handler_general import Tool_Handler
from Agents.agent_tools.utils.next_tool import next_task
from Agents.logg.logger import logger



def run_agent(agent_name,client,input_prompt,add_client1=None):
    logger.info(f"{agent_name} -- Initiated")
    for i in range(1000):  
        logger.info(f"{agent_name} -- Waiting for the Api Call ")
        logger.debug(f"{agent_name} -- Input Prompt for the llm on this API call ==> {input_prompt}")
        response_from_llm = client.generate_response(prompt=input_prompt)
        logger.info(f"{agent_name} -- Parsing the response of the Agent ")
        parsed_response = parse(response_from_llm,"Coding Agent")
        logger.debug(f"{agent_name} -- Parsed Response ==> {parsed_response}")
        if type(parsed_response) == dict:
            logger.info(f"{agent_name} -- Tool Handler")
            stat = Tool_Handler(parsed_response,f"{agent_name}")
        else:
            logger.warning(f"{agent_name} -- The LLm has produced not parsable xml")
            stat = {"to":"itself","content":parsed_response}

        if stat["to"] == "finish":
            break
        elif stat["to"] == "itself":
            input_prompt = stat["content"]
        elif stat["to"] == "user":
            #TODO has to create a function to return its response back to the user
            print(stat["content"])
            input_prompt = input("Enter your response: ")
            if input_prompt == "exit" or input_prompt == "Exit":
                break
        elif stat["to"] == "coder":
            logger.info(f"Coding Agent -- Finished Talking to -- {agent_name}")
            return stat["content"]

        elif stat["to"] == "specific_tool_handler":
            print(parsed_response)








