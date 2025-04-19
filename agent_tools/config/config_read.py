import json
import os
def load_config():
    # Get the folder where THIS script (config_read.py) is located
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, 'config.json')
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config

def save_config(new_config: dict):
    # Get the folder where THIS script is located
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, 'config.json')
    with open(config_path, 'w') as file:
        json.dump(new_config, file, indent=4)

def reset_api_key():
    js = load_config()
    js["openrouter_api_key"] = js["rate_limited_api_key"]
    js["rate_limited_api_key"] = []
    save_config(js)