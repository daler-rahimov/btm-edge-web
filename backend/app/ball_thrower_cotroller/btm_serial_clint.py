"""Used for communicating with Arduino over serial port"""

#TODO: Implement all 
class ArduinoBtm():
    def __init__ (self, serial_dev, baudrate):
        pass

    def set_spin(self) ->bool:
        """Set Spin from -100% (back-spin) to +100% (top-spin)

        Returns:
            bool : True if set False othervise   
        """
        return True 

    def get_spin(self) -> int:
        """Return spin in presentage -100% (back-spin) to +100% (top-spin)

        Returns:
            int: Spin in presentage  
        """
        return 10 

    def get_power(self) -> int:
        """Get power in presentage from 0% to 100% 

        Returns:
            int: Shot power in presentage  
        """
        return 10  

    def set_power(self) -> bool:
        """Set shot Power from 0%  to 100% 

        Returns:
            bool : True if set False othervise   
        """
