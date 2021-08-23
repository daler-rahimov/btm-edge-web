from .btm_serial_clint import ArduinoBtm
import logging 
logger = logging.getLogger(__name__)


class BallThrower():
    def __init__(self, btm_serial_api: ArduinoBtm):
        self.btm_serial_api = btm_serial_api

    def set_spin(self, spin: int) -> bool:
        """Set ball spin from 100% back-spin to 100% top-spin

        Returns:
            bool: True if was able to set False otherwise
        """
        logger.error("Spin = {}".format(spin))
        return True 

    def set_power(self, power: int) -> bool:
        """Set power of all the shots from 0% to 100%

        Returns:
            bool: True if was able to set False otherwise
        """
        return True

    def get_spin(self) -> int:
        """Return spin from -100% to +100%

        Returns:
            int: spin in presentage
        """
        # raise SerialException("Serial message")
        return self.btm_serial_api.get_spin()


    def get_power(self) -> int:
        """Get power of all the shots from 0% to 100%

        Returns:
            shot_power:  currelnly set shot power 
        """
        return self.btm_serial_api.get_power()
