from app.api.api_v1.routers import ball_thrower
from fastapi import FastAPI, Depends
from starlette.requests import Request
import uvicorn

from app.api.api_v1.routers.users import users_router
from app.api.api_v1.routers.auth import auth_router
from app.api.api_v1.routers.ball_thrower import ball_thrower_route 
from app.core import config
from app.db.session import SessionLocal
from app.core.auth import get_current_active_user
import app.ball_thrower_cotroller as ball_thrower_api 

app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api"
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.get("/api/v1")
async def root():
    return {"message": "Hello World"}


# Routers
app.include_router(
    users_router,
    prefix="/api/v1",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    ball_thrower_route,
    prefix="/api/v1/ball_thrower",
    tags=["ball_thrower"],
    dependencies=[Depends(get_current_active_user)],
)

@app.on_event("startup")
def init_stuff() -> None:
    ball_thrower_api.init()

@app.on_event("shutdown")
def shutdown_event():
    ball_thrower_api.discruct()

app.include_router(auth_router, prefix="/api", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)