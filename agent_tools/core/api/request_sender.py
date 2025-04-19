import requests
from Agents.agent_tools.config.config_read import load_config,save_config
import json
import time
from Agents.logg.logger import logger


def get_api_key(current_api_key=True):
    if current_api_key:
        t_api_key = load_config()["openrouter_api_key"][0]
        return t_api_key
    else:
        js = load_config()
        rep_api_key = js["openrouter_api_key"].pop(0)
        js["rate_limited_openrouter_api_key"].append(rep_api_key)
        save_config(js)
        return rep_api_key
        
def get_api_key_google(current_api_key=True):
    if current_api_key:
        t_api_key = load_config()["google_api_key"][0]
        return t_api_key
    else:
        js = load_config()
        rep_api_key = js["google_api_key"].pop(0)
        js["rate_limited_google_api_key"].append(rep_api_key)
        save_config(js)
        return rep_api_key


def handle_request(base_url,model,msg_his):
    api_key = get_api_key()
    response = requests.post(
    url=base_url,
    headers={
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    },
    data=json.dumps({
        #meta-llama/llama-4-scout:free
        "model": model, # Optional
        "messages": msg_his
    })
    )
    #error code finding
    try:
        error_code = response.json()["error"]["code"]
    except:
        error_code = 200

    if error_code == 429:
        logger.warning("Rate Limit Exceeded :: Changing Api Key")
        api_key = get_api_key(False)
        logger.warning("Rate Limit Exceeded :: Api Key Changed")
        return handle_request(base_url=base_url,model=model,msg_his=msg_his)
    elif error_code == 503:
        for i in range(0,25,5):
            logger.warning(f"Provider Time Out :: Time remaining : {25-i}")
            time.sleep(5)
        logger.warning("Provider Time Out :: Retrying Api Call")
        return handle_request(base_url=base_url,model=model,msg_his=msg_his)
    else:
        return response.json()

def handle_request_google(base_url,model,msg_his):
    api_key = get_api_key_google()
    response = requests.post(
    url=base_url,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    },
    data=json.dumps({
        #meta-llama/llama-4-scout:free
        "model": model, # Optional
        "messages": msg_his
    })
    )
    #error code finding
    try:
        error_code = response.json()[0]["error"]["code"]
    except:
        error_code = 200

    if error_code == 429:
        if "PerModelPerMinute" in response.json()[0]["error"]["details"][0]["violations"][0]["quotaId"]:
            sec = int(response.json()[0]["error"]["details"][2]["retryDelay"][:-1])
            logger.warning(f"Rate limit exceeded :: Waiting {sec} seconds")
            time.sleep(sec)
            return handle_request_google(base_url=base_url,model=model,msg_his=msg_his)
        else:
            logger.warning("Rate Limit Exceeded :: Changing Api Key")
            api_key = get_api_key_google(False)
            logger.warning("Rate Limit Exceeded :: Api Key Changed")
            return handle_request_google(base_url=base_url,model=model,msg_his=msg_his)
    else:
        return response.json()

