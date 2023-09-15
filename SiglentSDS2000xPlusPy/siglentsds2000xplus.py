import time
import vxi11

class SiglentSDS2000XPlus(vxi11.Instrument):
    _name = "Siglent SDS2000X Plus"

    def __init__(self, host, *args, **kwargs) -> None:
        super(SiglentSDS2000XPlus, self).__init__(host, *args, **kwargs)
        idn = self.idn.split(',')
        self.vendor = idn[0]
        self.product = idn[1]
        self.serial = idn[2]
        self.firmware = idn[3]


    def query(self, message, *args, **kwargs):
        """
        Write a message to the scope and read back the answer.
        See :py:meth:`vxi11.Instrument.ask()` for optional parameters.
        """
        return self.ask(message, *args, **kwargs)
    
    @property
    def idn(self):
        """
        The ``*IDN?`` string of the device.
        Will be fetched every time you access this property.
        """
        return self.query("*IDN?")

    def default_setup(self):
        pass