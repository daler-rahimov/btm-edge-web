from fastapi import APIRouter, Request, Depends, Response, Form, Body, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import typing as t
from serial import SerialException

# from app.core.auth import get_current_active_user, get_current_active_superuser
from app.ball_thrower_cotroller.ball_thrower import BallThrower
from app.ball_thrower_cotroller.btm_serial_clint import ArduinoBtm

ball_thrower_route = r = APIRouter()

btm_serial_api = ArduinoBtm("COM1", 19200)
ball_thrower = BallThrower(btm_serial_api)

class Power(BaseModel):
    shot_power: int = Field(..., gt=-1, lt=101, 
                description="Shot power value from"
            )

class Spin(BaseModel):
    spin: int = Field(..., gt=-101, lt=101, 
                description="Spin value from"
            )

class Message(BaseModel):
    message: str

class SerialMessage(BaseModel):
    message: str
    serial_message: str

SER_ERROR_CODE = 333
serial_com_error = {
    SER_ERROR_CODE: {
        "model": SerialMessage,
        "description": "Serial Comunication Error",
        }
}

serial_com_error_503= {
    SER_ERROR_CODE: serial_com_error.get(SER_ERROR_CODE),
    status.HTTP_503_SERVICE_UNAVAILABLE: {"model": Message}
}

@r.get( "/spin", response_model=Spin, responses=serial_com_error)
async def get_spin():
    """
    Get current set spin from -100% (which is back-spin) to +100% ( which is top-spin)
    """
    try:
        spin = Spin(spin=ball_thrower.get_spin())
    except SerialException as ex:
        return JSONResponse(status_code=SER_ERROR_CODE, content={
                "message": "Serial communication error. Check connection and try again",
                "serial_message": str(ex)
            }
        )
    else:
        return spin 


@r.put("/spin", responses=serial_com_error_503)
async def set_spin(spin: Spin = Body(...)):
    """
    Set current set spin from -100% (which is back-spin) to +100% ( which is top-spin)
    """
    try:
        if not ball_thrower.set_spin(spin.spin):
            return JSONResponse(status_code=503, content={
                "message": "Was not able to set 'SPIN'. Try again!"})
    except SerialException as ex:
        return JSONResponse(status_code=SER_ERROR_CODE, content={
                "message": "Serial communication error. Check connection and try again",
                "serial_message": str(ex)
            }
        )
    else:
        return spin 

@r.get( "/power", response_model=Power, responses=serial_com_error)
async def get_power():
    """
    Get currently set shot power from 0% to 100% 
    """
    try:
        power = Power(shot_power=ball_thrower.get_power())
    except SerialException as ex:
        return JSONResponse(status_code=SER_ERROR_CODE, content={
                "message": "Serial communication error. Check connection and try again",
                "serial_message": str(ex)
            }
        )
    else:
        return power 


@r.put("/power", responses=serial_com_error_503)
async def set_power(power: Power= Body(...)):
    """
    Set currently shot power from 0% to 100% 
    """
    try:
        if not ball_thrower.set_power(power.shot_power):
            return JSONResponse(status_code=503, content={
                "message": "Was not able to set 'SHOT POWER'. Try again!"})
    except SerialException as ex:
        return JSONResponse(status_code=SER_ERROR_CODE, content={
                "message": "Serial communication error. Check connection and try again",
                "serial_message": str(ex)
            }
        )
    else:
        return power 


# @r.get(
#     "/users/{user_id}",
#     response_model=User,
#     response_model_exclude_none=True,
# )
# async def user_details(
#     request: Request,
#     user_id: int,
#     db=Depends(get_db),
#     current_user=Depends(get_current_active_superuser),
# ):
#     """
#     Get any user details
#     """
#     user = get_user(db, user_id)
#     return user
#     # return encoders.jsonable_encoder(
#     #     user, skip_defaults=True, exclude_none=True,
#     # )


# @r.post("/users", response_model=User, response_model_exclude_none=True)
# async def user_create(
#     request: Request,
#     user: UserCreate,
#     db=Depends(get_db),
#     current_user=Depends(get_current_active_superuser),
# ):
#     """
#     Create a new user
#     """
#     return create_user(db, user)


# @r.put(
#     "/users/{user_id}", response_model=User, response_model_exclude_none=True
# )
# async def user_edit(
#     request: Request,
#     user_id: int,
#     user: UserEdit,
#     db=Depends(get_db),
#     current_user=Depends(get_current_active_superuser),
# ):
#     """
#     Update existing user
#     """
#     return edit_user(db, user_id, user)


# @r.delete(
#     "/users/{user_id}", response_model=User, response_model_exclude_none=True
# )
# async def user_delete(
#     request: Request,
#     user_id: int,
#     db=Depends(get_db),
#     current_user=Depends(get_current_active_superuser),
# ):
#     """
#     Delete existing user
#     """
#     return delete_user(db, user_id)
