"""Used for communicating with Arduino over serial port"""
import serial
import logging 
import threading
logger = logging.getLogger(__name__)


class ArduinoBtmClint():
    _instances = [] # All instance of this class
    _lock = threading.Lock()

    def __init__ (self, serial_dev):

        if not hasattr(self, "serial_con") :
            self._serial_con = serial.Serial()
            self._serial_con.port = serial_dev
            self._serial_con.baudrate = 115200


    def open_serial_port(self):
        try:
            if not self._serial_con.is_open:
                self._serial_con.open()
        except Exception as ex: 
            logger.error("Was not able to open or reopen serial connection: {}"
                .format(self._serial_con.port), exc_info=True)
        finally:
            logger.info("Serial connection to {} ... successful.".format(self._serial_con.port))

    def close_serial_port(self):
        try:
            if self._serial_con.is_open:
                self._serial_con.close()
        except: 
            logger.error("Was not able to close serial port", exc_info=True)
            
    def __new__(cls, *args, **kwargs):
        if len(kwargs) > 0:
            raise TypeError(
                f"{cls}. only allows positional arguments. Found "
                f"the following keyword arguments: {kwargs}"
            )
        instance = None
        with cls._lock:
            for i in cls._instances:
                if i.serial_con.port == args[0]: # if trying to open same port again 
                    instance = i 
            if instance == None:
                instance = super(ArduinoBtmClint, cls).__new__(cls)
                cls._instances.append(instance)
        return instance

    
    def __del__(self):
        if self._serial_con:
            if self._serial_con.is_open:
                self._serial_con.close()

    
    def send_cmd(self, cmd_arduino: list) -> int:
        """Send cmd to Arduino and get returned value 

        Args:
            cmd_arduino (list): API command to arduino/motor controller  

        Returns:
            int: value that is retured from Arduino  
        """
        logger.info("cmd given: {}".format(cmd_arduino))
        self._serial_con.write(cmd_arduino)
        r_bytes = self._serial_con.read(1)
        r_code = ArduinoBtmClint.to_int8(r_bytes[0])
        return r_code 
