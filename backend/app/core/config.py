import logging
import os
from functools import lru_cache
from pydantic import BaseSettings
import logging
logger = logging.getLogger(__name__)


CONF_NAME = os.getenv("CONFIG_NAME")
class APISettingsProd(BaseSettings):
    PROJECT_NAME = "btm_web"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    DOCS_URL: str = "/api/docs"
    API_V1_STR: str = "/api/v1"
    OPENAPI_ROUTE: str = "/api/"
    DEBUG: bool = False 
    DEBUG_EXCEPTIONS: bool = False
    RELAOD: bool = False
    ENV_NAME: str = CONF_NAME
    
    LOGGING_CONFIG = {
        "path": "/var/logs",
        "filename": "access.log",
        "level": "info",
        "rotation": "2 days",
        "retention": "1 months",
        # "format": "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
        "format": "<level>{level: <8}</level> - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    }


class APISettingsDevel(APISettingsProd):
    DEBUG: bool = True 
    DEBUG_EXCEPTIONS: bool = True
    RELAOD: bool = True 
   
    LOGGING_CONFIG = {
        "path": "/var/logs",
        "filename": "access.log",
        "level": "debug",
        "rotation": "1 days",
        "retention": "1 days",
        "format": "<level>{level: <8}</level> - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    }


class APISettingsTest(APISettingsProd):
    pass


@lru_cache()
def get_app_settings() -> APISettingsProd:
    if CONF_NAME == 'prod' or CONF_NAME == None:
        return APISettingsProd()  # reads variables from environment
    elif CONF_NAME == 'devel':
        return APISettingsDevel()  # reads variables from environment
    elif CONF_NAME == 'test':
        return APISettingsTest 
