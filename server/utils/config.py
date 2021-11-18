import os
import json

ENV_HOME = os.environ['ENV_HOME']
APP_NAME = "sparkbase"

LOG_DIR     = os.path.join(ENV_HOME, "logs", APP_NAME)
CFG_DIR     = os.path.join(ENV_HOME, "configs", APP_NAME)
DATA_DIR    = os.path.join(ENV_HOME, "data", APP_NAME)

def get_config_json(name):
    with open(os.path.join(CFG_DIR, name), "rt") as f:
        return json.load(f)

