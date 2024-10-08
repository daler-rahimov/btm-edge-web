"""Used in order to decuple serial communication for testing"""
import logging 
import bitstring
from serial import SerialException
from .btm_serial_clint import ArduinoBtmClint
logger = logging.getLogger(__name__)

# Arduino CMD prefixes 
CMD_SOH = 0x01 # starting byte  
CMD_ETX = 0x03 # ending byte 
CMD_PER_POWER=	ord("p")
CMD_PER_SPIN = 	ord("s")
CMD_PER_MODE =	ord("m")
CMD_PER_VER  = 	ord("v")
CMD_PER_GET  =	ord("g")
CMD_PER_SET  = 	ord("s")

ERROR_EXPLANATION = {
    -1: "There was an internal error",
    -2: "No such Shot",
    -3: "Command incorrect format ",
    -4: "Partial command was given",
    -5: "Mode was not set",
    -6: "No such command",
    -7: "Not implemented",
    -8: "Incorrect value given for Set command",
}

class BallThrower():
    def __init__(self, btm_serial_api: ArduinoBtmClint):
        self.btm_serial_api = btm_serial_api

    def set_spin(self, spin: int):
        """Set Spin from -100% (back-spin) to +100% (top-spin)
       
        Raises:
            SerialException: If Motor controller returns error. Includes a message as well
        """
        if spin > 100 or spin < -100: 
            raise SerialException(
                "Invalid Spin value. Can be from -100% (back-spin) to +100% (top-spin)."
                "Given value: {}".format(spin))
        cmd_arduino = [CMD_SOH, CMD_PER_SET, CMD_PER_SPIN, spin, CMD_ETX]
        self.send_cmd(cmd_arduino)


    def set_power(self, power):
        """Set shot Power from 0%  to 100% 

        Raises:
            SerialException: If Motor controller returns error. Includes a message as well
        """
        if power > 100: 
            raise SerialException(
                "Invalid power value. Can be from from 0%  to 100%. "
                "Given value: {}".format(power))
        cmd_arduino = [CMD_SOH, CMD_PER_SET, CMD_PER_POWER, power, CMD_ETX]
        self.send_cmd(cmd_arduino)


    def get_spin(self) -> int:
        """Return spin in presentage -100% (back-spin) to +100% (top-spin)

        Returns:
            int: Spin in presentage  
        Raises:
            SerialException: error with the message  
        """
        cmd_arduino = [CMD_SOH, CMD_PER_GET, CMD_PER_SPIN, 0, CMD_ETX]
        return self.send_cmd(cmd_arduino)


    def get_power(self) -> int:
        """Get power in presentage from 0% to 100% 

        Returns:
            int: Shot power in presentage  
        Raises:
            SerialException: error with the message  
        """
        cmd_arduino = [CMD_SOH, CMD_PER_GET, CMD_PER_POWER, 0, CMD_ETX]
        return self.send_cmd(cmd_arduino)


    @staticmethod
    def to_int8(byte: int ) -> int:
        bit = bitstring.Bits(uint=byte, length=8)
        return bit.unpack('int')[0]


    def check_arduino_error(self, r_code: int):
        """Check arduino code returned and raise exception if there was an error

        Args:
            r_code (int): Return code from arduino  

        Raises:
            SerialException: error with the message  
        """
        if r_code in ERROR_EXPLANATION:
            raise SerialException(ERROR_EXPLANATION[r_code])


    def send_cmd(self, cmd_arduino: list) -> int:
        """Send cmd to Arduino and get returned value 

        Args:
            cmd_arduino (list): API command to arduino/motor controller  

        Returns:
            int: value that is retured from Arduino. If negative raise exception 
        """
        r_code = self.btm_serial_api.send_cmd(cmd_arduino)
        self.check_arduino_error(r_code)
        return r_code 