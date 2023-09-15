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
        """The command query identifies the instrument type and software version. The 
        response consists of four different fields providing information on the 
        manufacturer, the scope model, the serial number and the firmware revision.

        :return: Siglent Technologies,<model>,<serial_number>,<firmware>
        """
        return self.query("*IDN?")
    
    def autosetup(self):
        """ This command attempts to automatically adjust the trigger, vertical, and 
        horizontal controls of the oscilloscope to deliver a usable display of the 
        input signal. Autoset is not recommended for use on low frequency events 
        (< 100 Hz).

        :return: Nothing
        """
        return self.write(":AUToset")
    
    def set_single_trigger(self):
        """The backlight of SINGLE key lights up, the oscilloscope enters the 
        waiting trigger state and begins to search for the trigger signal that meets 
        the conditions. If the trigger signal is satisfied, the running state shows 
        Trig'd, and the interface shows stable waveform. Then, the oscilloscope stops 
        scanning, the RUN/STOP key becomes red, and the running status shows Stop. 
        Otherwise, the running state shows Ready, and the interface does not display 
        the waveform.

        :return: Nothing
        """
        return self.write(":TRIGger:MODE SINGle")
    
    def set_normal_trigger(self):
        """The oscilloscope enters the wait trigger state and begins to search for 
        trigger signals that meet the conditions. If the trigger signal is satisfied, 
        the running state shows Trig'd, and the interface shows stable waveform. 
        Otherwise, the running state shows Ready, and the interface displays the last 
        triggered waveform (previous trigger) or does not display the waveform (no 
        previous trigger).

        :return: Nothing
        """
        return self.write(":TRIGger:MODE NORMal")
    
    def set_auto_trigger(self):
        """The oscilloscope begins to search for the trigger signal that meets the 
        conditions. If the trigger signal is satisfied, the running state on the top 
        left corner of the user interface shows Trig'd, and the interface shows stable 
        waveform. Otherwise, the running state always shows Auto, and the interface 
        shows unstable waveform.

        :return: Nothing
        """
        return self.write(":TRIGger:MODE AUTO")
    
    def set_force_trigger(self):
        """Force to acquire a frame regardless of whether the input signal meets the 
        trigger conditions or not.

        :return: Nothing
        """
        return self.write(":TRIGger:MODE FTRIG")

    def default_setup(self):
        pass