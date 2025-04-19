from Agents.agent_tools.utils.file_operations.create_and_write_file import write_to_file
from Agents.agent_tools.utils.text_operations.regex_search import search_files
from Agents.agent_tools.utils.file_operations.read_file import read_file
from Agents.agent_tools.utils.file_operations.list_files import list_files
from Agents.agent_tools.utils.file_operations.replace_lines import search_and_replace
from Agents.agent_tools.core.function.ask_designer import ask_question_to_designer
from Agents.agent_tools.utils.image_operations.read_images import read_image
from Agents.agent_tools.utils.file_operations.path_normalizer import correct_path
from Agents.agent_tools.utils.image_operations.placeholder_image import placeholder_image
from Agents.agent_tools.utils.next_tool import next_task
from Agents.logg.logger import logger
from Agents.client import get_coder_vision_client

#Not Completed tools ==> execute_command, vision_query
#completed tools ==> write_to_file,plan_mode_respond, ask_followup_question, search_files, read_file, list_files, attempt_completion, replace_in_file, path_normalizer, read_images

def Actual_tool_handler(parsed_xml,agent):
    tools_used = parsed_xml.keys()
    has_tool_used = False
    if "write_to_file" in tools_used:
        logger.info(f"{agent} -- Using write_to_file")
        path = correct_path(parsed_xml["write_to_file"]["path"])
        content = parsed_xml["write_to_file"]["content"]
        has_tool_used = True
        return {"to":"itself","content":write_to_file(path,content,f"{agent}")}
        
    if "ask_followup_question" in tools_used:
        #change to the ask question to agent when finished prototyping (ACT)
        logger.info(f"{agent} -- Using ask_followup_question")
        query = parsed_xml["ask_followup_question"]["question"] + "\n "
        if "options" in parsed_xml["ask_followup_question"]:
            query += parsed_xml["ask_followup_question"]["options"]
        has_tool_used = True
        return {"to":"itself","content":ask_question_to_designer()}

    if "plan_mode_respond" in tools_used:
        #change to the ask question to agent when finished prototyping (ACT)
        logger.info(f"{agent} -- Using plan_mode_respond")
        query = parsed_xml["plan_mode_respond"]["response"] + "\n "
        if "options" in parsed_xml["plan_mode_respond"]:
            query += parsed_xml["plan_mode_respond"]["options"]
        has_tool_used = True
        return {"to":"itself","content":ask_question_to_designer(query)}

    if "search_files" in tools_used:
        logger.info(f"{agent} -- Using search_files")
        path = correct_path(parsed_xml["search_files"]["path"])
        regex = parsed_xml["search_files"]["regex"]
        if "file_pattern" in parsed_xml["search_files"]:
            file_pattern = parsed_xml["search_files"]["file_pattern"]
        else:
            file_pattern = "*"
        has_tool_used = True
        return {"to":"itself","content":search_files(path,regex,file_pattern,f"{agent}")}

    if "read_file" in tools_used:
        logger.info(f"{agent} -- Using read_file")
        path = correct_path(parsed_xml["read_file"]["path"])
        has_tool_used = True
        return {"to":"itself","content":read_file(path,f"{agent}")}
    
    if "list_files" in tools_used:
        logger.info(f"{agent} -- Using list_files")
        path = correct_path(parsed_xml["list_files"]["path"])
        if "recursive" in parsed_xml["list_files"]:
            recursive = parsed_xml["list_files"]["recursive"]
        else:
            recursive = False
        has_tool_used = True
        return {"to":"itself","content":list_files(path,recursive,f"{agent}")}
    
    if "replace_in_file" in tools_used:
        logger.info(f"{agent} -- Using replace_in_file")
        path = correct_path(parsed_xml["replace_in_file"]["path"])
        diff = parsed_xml["replace_in_file"]["diff"]
        has_tool_used = True
        return {"to":"itself","content":search_and_replace(path,diff,f"{agent}")}

    if "attempt_completion" in tools_used:
        logger.info(f"{agent} -- Using attempt_completion")
        result = parsed_xml["attempt_completion"]["result"]
        if "command" in parsed_xml["attempt_completion"]:
            cmd = parsed_xml["attempt_completion"]["command"]
        else:
            cmd = ""
        has_tool_used = True
        if agent == "Coding Agent":
            if next_task() == "All tasks are completed!":
                return {"to":"finish","content":{"agent":agent,"result":result}}
            else:
                return {"to":"itself","content":next_task()}
        else:
            return {"to":"finish","content":{"agent":agent,"result":result}}
    
    if "read_image" in tools_used:
        logger.info(f"{agent} -- Using read_image")
        paths = [item.strip() for item in parsed_xml["read_image"]["path"].split(',')]
        paths = [correct_path(p) for p in paths]
        has_tool_used = True
        return {"to":"itself","content":read_image(paths,f"{agent}")}
    
    if "vision_query" in tools_used:
        logger.info(f"{agent} -- Using vision_query")
        query = parsed_xml["vision_query"]["query"]
        from Agents.run_agent import run_agent
        return {"to":"itself","content":run_agent("Vision Agent",get_coder_vision_client(),query)}

    if "talk_to_user" in tools_used:
        logger.info(f"{agent} -- Using Talk to user")
        query = parsed_xml["talk_to_user"]["query"]
        return {"to":"user","content":query}

    if "download_placeholder_image" in tools_used:
        logger.info("Vision Agent -- Using download_placeholder_image")
        path = correct_path(parsed_xml["download_placeholder_image"]["path"])
        keywords = parsed_xml["download_placeholder_image"]["keywords"]
        orient = parsed_xml["download_placeholder_image"]["orientation"]
        return {"to":"itself","content":placeholder_image(path,keywords,orient,"Vision Agent")}
    
    if "respond_coder" in tools_used:
        logger.info("Vision Agent -- Using respond_coder")
        logger.info("Vision Agent -- Submiting Response to -- Coding Agent")
        response = parsed_xml["respond_coder"]["response"]
        print(response)
        return{"to":"coder","content":response}

    if "next_task" in tools_used:
        has_tool_used = True
        return {"to":"itself","content":next_task()}

    if not has_tool_used:
        logger.info(f"{agent} -- No Tool has been used")
        return {"to":"itself","content":"""THE RESULT YOU HAVE PROVIDED IS UNABLE TO PARSE.KINDLY FOLLOW THE CORRECT SYNTAX# Reminder: Instructions for Tool Use

        Tool uses are formatted using XML-style tags. The tool name is enclosed in opening and closing tags, and each parameter is similarly enclosed within its own set of tags. Here's the structure:

        <tool_name>
        <parameter1_name>value1</parameter1_name>
        <parameter2_name>value2</parameter2_name>
        ...
        </tool_name>

        For example:

        <plan_mode_respond>
        <response><![CDATA[Your response here]]></response>
        <options>
        <![CDATA[Set of options here (optional), e.g. Option 1 , Option 2 , Option 3.]]>
        </options>
        </plan_mode_respond>

        Always adhere to this format for all tool uses to ensure proper parsing and execution."""}


def Tool_Handler(parsed_xml,agent):
    try:
        return Actual_tool_handler(parsed_xml,agent)
    except:
        return {"to":"itself","content":"""THE RESULT YOU HAVE PROVIDED IS UNABLE TO PARSE.KINDLY FOLLOW THE CORRECT SYNTAX# Reminder: Instructions for Tool Use

        Tool uses are formatted using XML-style tags. The tool name is enclosed in opening and closing tags, and each parameter is similarly enclosed within its own set of tags. Here's the structure:

        <tool_name>
        <parameter1_name>value1</parameter1_name>
        <parameter2_name>value2</parameter2_name>
        ...
        </tool_name>

        For example:
        ## Example 1
        <plan_mode_respond>
        <response><![CDATA[Your response here]]></response>
        <options>
        <![CDATA[Set of options here (optional), e.g. Option 1 , Option 2 , Option 3.]]>
        </options>
        </plan_mode_respond>
        ##Example 2
        <read_image>  
            <path><![CDATA[path/to/image1.png]]></path>  
        </read_image>
        Always adhere to this format for all tool uses to ensure proper parsing and execution."""}