from Agents.agent_tools.core.api.response import OpenRouter_Client,Google_Client
from Agents.agent_tools.config.config_read import load_config
from Agents.logg.logger import logger
coder_client = None
coder_vision_client = None
page_detector_client = None
ui_designer_client = None
task_manager_client = None

coder_system_prompt_path = "Agents/agent_tools/prompts/coder_system_prompt.txt"
vision_system_prompt_path = "Agents/agent_tools/prompts/coder_vision_system_prompt.txt"
page_detector_system_prompt_path = "Agents/agent_tools/prompts/pagedetector_system_prompt.txt"
ui_designer_system_prompt_path = "Agents/agent_tools/prompts/ui_designer_system_prompt.txt"
task_manager_agent_system_prompt_path = "Agents/agent_tools/prompts/task_master_system_prompt.txt"


def initialize_clients(*args, **kwargs):

    #SYSTEM PROMPTS
    try:
        with open(coder_system_prompt_path,"r", encoding='utf-8') as f:
            coder_system_prompt = f.read()
        with open(vision_system_prompt_path,"r", encoding='utf-8') as f:
            system_prompt = f.read()
        with open(page_detector_system_prompt_path,"r", encoding='utf-8') as f:
            page_detector_system_prompt = f.read()
        with open(ui_designer_system_prompt_path,"r", encoding='utf-8') as f:
            ui_designer_system_prompt = f.read()
        with open(task_manager_agent_system_prompt_path,"r", encoding='utf-8') as f:
            task_manager_agent_system_prompt = f.read()
        #INITIALIZE CLIENTS
        global coder_client,coder_vision_client,page_detector_client,ui_designer_client,task_manager_client
        coder_client = Google_Client(model=load_config()["coding_model"],
                            api_key=load_config()["openrouter_api_key"][0],
                            base_url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
                            system_prompt=coder_system_prompt)
        coder_vision_client = Google_Client(model=load_config()["vision_model"],
                                api_key=load_config()["openrouter_api_key"][0],
                                base_url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
                                system_prompt=system_prompt)
        page_detector_client = Google_Client(model=load_config()["page_detector_model"],
                            api_key=load_config()["openrouter_api_key"][0],
                            base_url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
                            system_prompt=page_detector_system_prompt)
        ui_designer_client = Google_Client(model=load_config()["ui_detector_model"],
                                api_key=load_config()["openrouter_api_key"][0],
                                base_url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
                                system_prompt=ui_designer_system_prompt)
        task_manager_client = Google_Client(model=load_config()["task_manager_model"],
                                api_key=load_config()["openrouter_api_key"][0],
                                base_url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
                                system_prompt=task_manager_agent_system_prompt)
        logger.info("Initialized Clients Successfully")
    except Exception as e:
        logger.critical(f"Client Initialize Failed with error ==> {e}")
    
def get_coder_client():
    if coder_client is None:
        raise RuntimeError("Client not initialized. Call initialize_clients() first")
    return coder_client

def get_coder_vision_client():
    if coder_vision_client is None:
        raise RuntimeError("Client not initialized. Call initialize_clients() first")
    return coder_vision_client

def get_page_detector_client():
    if page_detector_client is None:
        raise RuntimeError("Client not initialized. Call initialize_clients() first")
    return page_detector_client

def get_ui_designer_client():
    if ui_designer_client is None:
        raise RuntimeError("Client not initialized. Call initialize_clients() first")
    return ui_designer_client
    
def get_task_manager_client():
    if task_manager_client is None:
        raise RuntimeError("Client not initialized. Call initialize_clients() first")
    return task_manager_client
