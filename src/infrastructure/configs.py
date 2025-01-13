import os
from dynaconf import Dynaconf

def load_config():
    settings = Dynaconf(
        settings_files=[os.environ['CONFIG_PATH'], os.environ['SECRETS_PATH']], )
    
    return settings
