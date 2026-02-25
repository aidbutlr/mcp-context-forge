# Standard
import os
from pathlib import Path
import sys

# Third-Party
from jwcrypto import jwe, jwk

project_root = Path(__file__).resolve().parents[1]  # adjust as needed
sys.path.insert(0, str(project_root)+"/cyberfraud")
# Third-Party
import protected_secrets

protected_secrets_dict=protected_secrets.get_config()
_real_getenv = os.environ.get



protected_secrets_map ={
    "POSTGRES_PASSWORD": "PG__PASSWORD",
    "POSTGRES_USER":"PG__USERNAME",
    "REDIS_PASSWORD":"REDIS__PASSWORD",
    "BASIC_AUTH_USER":"BASICAUTH__USERNAME",
    "BASIC_AUTH_PASSWORD":"BASICAUTH__PASSWORD",
    "PYDANTIC_DISABLE_PLUGINS":"PYDANTIC__DISABLE_PLUGINS",
    }

def custom_getenv(key, default=None):    
    if key in protected_secrets_map:
        print(f">>>>Getting Protected Secret {key}")
        ps_path = protected_secrets_map[key]
        nodes = ps_path.split("__")
        loc =protected_secrets_dict
        for node in nodes:
            if node in loc:
                loc = loc[node]
            else:
                print(f"Entry not found in Protected Secrets {node}")
                break
        return loc
        return protected_secrets_dict
    else:
        #print(f">>>>Getting Environment Secret {key}")
        return _real_getenv(key, default)

os.environ.get = custom_getenv
