# Standard
import os
from typing import Any

# Local
from . import protected_secrets

protected_secrets_dict: dict[Any, Any]=protected_secrets.get_config()


protected_secrets_map: dict[str, str] ={
    "POSTGRES_PASSWORD": "PG__PASSWORD",
    "POSTGRES_USER": "PG__USERNAME",
    "POSTGRES_HOST": "PG__HOST",
    "POSTGRES_PORT": "PG__PORT",
    "REDIS_HOST": "REDIS__HOST",
    "REDIS_PORT": "REDIS__PORT",
    "REDIS_PASSWORD": "REDIS__PASSWORD",
    "BASIC_AUTH_USER": "systemadminuser__admin_username",
    "BASIC_AUTH_PASSWORD": "systemadminuser__admin_password",
    "PLATFORM_ADMIN_EMAIL": "systemadminuser__admin_email",
    "PLATFORM_ADMIN_PASSWORD": "systemadminuser__admin_password"
    }


def read_protected_secrets() -> None:
    """Load protected secrets from cyberfraud config into environment variables.
    
    Reads secrets from the protected_secrets_dict using paths defined in
    protected_secrets_map and sets them as environment variables.
    """
    print("Protected secrets map:")
    for env_var, secret_path in protected_secrets_map.items():
        print(f"  {env_var} -> {secret_path}")
    for key in protected_secrets_map:
        print(f">>>>Getting Protected Secret {key}")
        ps_path = protected_secrets_map[key]
        ps_path = ps_path.lower()
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
        os.environ[key]=str(value)
        
    if os.environ["DATABASE_URL"]:
        os.environ["DATABASE_URL"] = os.path.expandvars(os.environ["DATABASE_URL"])
        print(f"DATABASE_URL: {os.environ['DATABASE_URL']}")
    if os.environ["REDIS_URL"]:
        os.environ["REDIS_URL"] = os.path.expandvars(os.environ["REDIS_URL"])
        print(f"REDIS_URL: {os.environ['REDIS_URL']}")

        
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
