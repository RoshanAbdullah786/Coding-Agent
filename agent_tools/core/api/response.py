import requests
import json
from Agents.logg.logger import logger
from Agents.agent_tools.config.config_read import load_config
import time
from Agents.agent_tools.core.api.request_sender import handle_request,handle_request_google


class OpenRouter_Client():
    def __init__(self, model= "openrouter/optimus-alpha" ,api_key: str = None, base_url: str = "https://openrouter.ai/api/v1/chat/completions",system_prompt = None):
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.message_history = [{"role": "system","content":self.system_prompt}]
        self.api_no = 0
        self.retry_count = 0
    
    def update_message_history(self,message):
        logger.debug(f"Message to be updated in the message history ==> {message}")
        logger.debug(f"Message History befor updatation == > {self.message_history}")
        if type(message) == dict:
            if message["role"] == "assistant" or message["role"] == "user":
                self.message_history.append({"role":message["role"],"content":message["content"]})
        else:
            self.message_history.append({"role": "user","content":message})
        logger.debug(f"Message History after updation ==> {self.message_history}")

    def generate_response(self,prompt,update=True):
        if update:
            self.update_message_history(prompt)
        try:
            response = handle_request(self.base_url,self.model,self.message_history)
            self.update_message_history(response["choices"][0]['message'])
            logger.debug("Api Call Succesfully Received")
            return response["choices"][0]['message']['content']
        except Exception as e:
            logger.debug(response)
            logger.exception("An Error Occured")

class Google_Client():
    def __init__(self, model= "openrouter/optimus-alpha" ,api_key: str = None, base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",system_prompt = None):
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.message_history = [{"role": "system","content":self.system_prompt}]
        self.api_no = 0
        self.retry_count = 0
    
    def update_message_history(self,message):
        logger.debug(f"Message to be updated in the message history ==> {message}")
        logger.debug(f"Message History befor updatation == > {self.message_history}")
        if type(message) == dict:
            if message["role"] == "assistant" or message["role"] == "user":
                self.message_history.append({"role":message["role"],"content":message["content"]})
        else:
            self.message_history.append({"role": "user","content":message})
        logger.debug(f"Message History after updation ==> {self.message_history}")

    def generate_response(self,prompt,update=True):
        if update:
            self.update_message_history(prompt)
        try:
            response = handle_request_google(self.base_url,self.model,self.message_history)
            self.update_message_history(response["choices"][0]['message'])
            logger.debug("Api Call Succesfully Received")
            return response["choices"][0]['message']['content']
        except Exception as e:
            logger.debug(response)
            logger.exception("An Error Occured")

