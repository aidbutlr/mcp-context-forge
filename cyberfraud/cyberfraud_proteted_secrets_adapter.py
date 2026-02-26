# Standard
import os
from typing import Any

# Local
from . import protected_secrets

protected_secrets_dict: dict[Any, Any]=protected_secrets.get_config()

protected_secrets_map: dict[str, str] ={
    "POSTGRES_PASSWORD": "PG__PASSWORD",
    "POSTGRES_USER": "PG__USERNAME",
    "REDIS_PASSWORD": "REDIS__PASSWORD",
    "BASIC_AUTH_USER": "BASICAUTH__USERNAME",
    "BASIC_AUTH_PASSWORD": "BASICAUTH__PASSWORD",
    }


def read_protected_secrets() -> None:
    """Load protected secrets from cyberfraud config into environment variables.
    
    Reads secrets from the protected_secrets_dict using paths defined in
    protected_secrets_map and sets them as environment variables. 
    """
    for key in protected_secrets_map:
        print(f">>>>Getting Protected Secret {key}")
        ps_path = protected_secrets_map[key]
        nodes: list[str] = ps_path.split(sep="__")
        value =""
        loc: Any =protected_secrets_dict
        for node in nodes:
            if node in loc:
                loc: Any = loc[node]
                value: Any = loc
            else:
                value=""
                print(f"Entry not found in Protected Secrets {node}")
                break
        os.environ[key]=value

        
read_protected_secrets()

"""


project_root = Path(__file__).resolve().parents[1]  # adjust as needed
sys.path.insert(0, str(project_root)+"/cyberfraud")
# Third-Party

_real_getenv = os.environ.get


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
"""
