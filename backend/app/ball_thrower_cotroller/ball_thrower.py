"""Used in order to decuple serial communication for testing"""
from .btm_serial_clint import ArduinoBtmClint
import logging 
logger = logging.getLogger(__name__)

class BallThrower():
    def __init__(self, btm_serial_api: ArduinoBtmClint):
        self.btm_serial_api = btm_serial_api

    def set_spin(self, spin: int) -> bool:
        """Set ball spin from 100% back-spin to 100% top-spin

        Returns:
            bool: True if was able to set False otherwise
        """
        return self.btm_serial_api.set_spin(spin) 

    def set_power(self, power: int) -> bool:
        """Set power of all the shots from 0% to 100%

        Returns:
            bool: True if was able to set False otherwise
        """
        return self.btm_serial_api.set_power(power) 

    def get_spin(self) -> int:
        """Return spin from -100% to +100%

        Returns:
            int: spin in presentage
        """
        return self.btm_serial_api.get_spin()


    def get_power(self) -> int:
        """Get power of all the shots from 0% to 100%

        Returns:
            shot_power:  currelnly set shot power 
        """
        return self.btm_serial_api.get_power()
