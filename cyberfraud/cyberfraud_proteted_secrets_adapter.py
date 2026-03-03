# Standard
import os
from typing import Any

# First-Party
from mcpgateway.services.logging_service import LoggingService
# Local
from . import protected_secrets

logging_service = LoggingService()
logger = logging_service.get_logger(__name__)

protected_secrets_dict: dict[Any, Any]=protected_secrets.get_config()


protected_secrets_to_env_map: dict[str, str] ={
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
    """
    Reads secrets from the protected_secrets_dict using paths defined in
    protected_secrets_to_env_map and sets them as environment variables.
    """
    logger.debug("Populating env from protected secrets")
    for env_var, secret_path in protected_secrets_to_env_map.items():
        logger.debug(f"  {env_var} -> {secret_path}")
    for key in protected_secrets_to_env_map:
        logger.debug(f"Getting Protected Secret {key}")
        ps_path = protected_secrets_to_env_map[key]
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
                logger.debug(f"Entry not found in Protected Secrets {node}")
                break
        os.environ[key]=str(value)
        
    if "DATABASE_URL" in os.environ:
        os.environ["DATABASE_URL"] = os.path.expandvars(os.environ["DATABASE_URL"])
        logger.debug(f"DATABASE_URL: {os.environ['DATABASE_URL']}")
    if "REDIS_URL" in os.environ:
        os.environ["REDIS_URL"] = os.path.expandvars(os.environ["REDIS_URL"])
        logger.debug(f"REDIS_URL: {os.environ['REDIS_URL']}")


if "USE_PROTECTED_SECRETS" in os.environ and os.environ["USE_PROTECTED_SECRETS"] == "True" :
    logger.info(f"Initializing Protected Secrets")
    read_protected_secrets()
