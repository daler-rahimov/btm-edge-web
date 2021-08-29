from .ball_thrower_core import BallThrower
from .btm_serial_clint import ArduinoBtmClint
import logging 
logger = logging.getLogger(__name__)

try:
    btm_serial_api = ArduinoBtmClint("COM4") # TODO: get this port name from config 
    ball_thrower = BallThrower(btm_serial_api)
except Exception as ex:
    logger.critical("Motor Controller connection error: {}".format(ex), exc_info=True)