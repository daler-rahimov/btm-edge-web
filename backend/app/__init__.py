# encoding: utf-8
"""
RESTful API Server.
"""
from fastapi import FastAPI
from fastapi import FastAPI, Depends
from app.api.api_v1.routers.users import users_router
from app.api.api_v1.routers.auth import auth_router
from app.api.api_v1.routers.ball_thrower import ball_thrower_route 
from app.core.auth import get_current_active_user
import app.ball_thrower_cotroller as ball_thrower_api 
import app.core.config as config
from app.core.custom_logging import CustomizeLogger
import logging 
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Entry point to the FastAPI Server application.
    """

    app_settings = config.get_app_settings()

    server = FastAPI(
        title=app_settings.PROJECT_NAME,
        docs_url=app_settings.DOCS_URL,
        openapi_url=app_settings.OPENAPI_ROUTE,
        debug=app_settings.DEBUG)

    # Loguru Logging
    logger = CustomizeLogger.make_logger(app_settings.LOGGING_CONFIG)
    server.logger = logger

    # check evn 
    if app_settings.ENV_NAME != None or app_settings.ENV_NAME != "prod":
        logger.warning("Not for production. Unset CONFIG_NAME env for prod! ")
        # Mocking Arduino device for easy of development
        import app.ball_thrower_cotroller as btm 
        from app.ball_thrower_cotroller.btm_serial_clint import ArduinoBtmClintMock
        btm.btm_serial_api = ArduinoBtmClintMock("COM4") 
        btm.ball_thrower = btm.BallThrower(btm.btm_serial_api)
    
    # Routers
    server.include_router(
        users_router,
        prefix="/api/v1",
        tags=["users"],
        dependencies=[Depends(get_current_active_user)],
    )
    server.include_router(
        ball_thrower_route,
        prefix="/api/v1/ball_thrower",
        tags=["ball_thrower"],
        dependencies=[Depends(get_current_active_user)],
    )

    server.include_router(auth_router, prefix="/api", tags=["auth"])

    # To make sure relaod does not open multiple serial cons
    @server.on_event("startup")  
    def init_stuff() -> None:
        ball_thrower_api.init()

    @server.on_event("shutdown")
    def shutdown_event():
        ball_thrower_api.discruct()

    return server
