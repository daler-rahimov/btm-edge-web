from fastapi import APIRouter, Request, Depends, Response, Form, Body, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import typing as t
from serial import SerialException
import logging 
logger = logging.getLogger(__name__)

ball_thrower_route = r = APIRouter()

# from app.core.auth import get_current_active_user, get_current_active_superuser
from app.ball_thrower_cotroller import ball_thrower


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
        "description": "Motor Controller Serial Port comunication error",
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
                "message": "Mottor Contoller communication error. Check connection and try again",
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
        ball_thrower.set_spin(spin.spin)
    except SerialException as ex:
        return JSONResponse(status_code=SER_ERROR_CODE, content={
                "message": "Mottor Contoller communication error. Check connection and try again",
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
                "message": "Mottor Contoller communication error. Check connection and try again",
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
        ball_thrower.set_power(power.shot_power)
    except SerialException as ex:
        return JSONResponse(status_code=SER_ERROR_CODE, content={
                "message": "Mottor Contoller communication error. Check connection and try again",
                "serial_message": str(ex)
            }
        )
    else:
        return power 

