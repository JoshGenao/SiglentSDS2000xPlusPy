import time
import vxi11
from enum import Enum

class SiglentWaveformWidth(Enum):
    BYTE = "BYTE"
    WORD = "WORD"


class SiglentSDS2000XPlus(vxi11.Instrument):
    _name = "Siglent SDS2000X Plus"

    def __init__(self, host, *args, **kwargs) -> None:
        super(SiglentSDS2000XPlus, self).__init__(host, *args, **kwargs)
        idn = self.idn.split(',')
        self.vendor = idn[0]
        self.product = idn[1]
        self.serial = idn[2]
        self.firmware = idn[3]
        self.memory_depth_values = (10000, 100000, 1000000, 10000000, 100000000,
                                    20000, 200000, 2000000, 20000000, 200000000)

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
    
    @property
    def trigger_status(self):
        """The command query returns the current state of the trigger.

        :return: str
                    Returns either "Arm", "Ready", "Auto", "Trig'd", "Stop", "Roll"
        """
        return self.query(":TRIGger:STATus?")
    
    @property
    def waveform_preamble(self):
        """The query returns the parameters of the source using by the command 
        :WAVeform:SOURce.
        """
        return self.query(":WAVeform:PREamble?")
    
    @property
    def timebase_scale(self) -> float:
        """The query returns the current horizontal scale setting in seconds per 
        division for the main window.

        :return: float

        """
        return float(self.query(":TIMebase:SCALe?"))
    
    @timebase_scale.setter
    def timebase_scale(self, new_timebase):
        """The command sets the horizontal scale per division for the main window.

        :param new_timebase: Value to set the horizontal timebase
        """
        self.write(":TIMebase:SCALe {}".format(new_timebase))

    @property
    def memory_depth(self) -> int:
        """The query returns the maximum memory depth.

        :return: int
                    Returns the maximum memory depth
        """
        return int(self.query(":ACQuire:MDEPth?"))
    
    @memory_depth.setter
    def memory_depth(self, mdepth: int):
        mdepth = min(self.memory_depth_values, key=lambda x:abs(x-mdepth))
        self.write(":ACQuire:MDEPth {}".format(mdepth))
    
    def autosetup(self):
        """ This command attempts to automatically adjust the trigger, vertical, and 
        horizontal controls of the oscilloscope to deliver a usable display of the 
        input signal. Autoset is not recommended for use on low frequency events 
        (< 100 Hz).

        :return: Nothing
        """
        self.write(":AUToset")
    
    def set_single_trigger(self):
        """The command sets the mode of the trigger.

        The backlight of SINGLE key lights up, the oscilloscope enters the 
        waiting trigger state and begins to search for the trigger signal that meets 
        the conditions. If the trigger signal is satisfied, the running state shows 
        Trig'd, and the interface shows stable waveform. Then, the oscilloscope stops 
        scanning, the RUN/STOP key becomes red, and the running status shows Stop. 
        Otherwise, the running state shows Ready, and the interface does not display 
        the waveform.

        :return: Nothing
        """
        self.write(":TRIGger:MODE SINGle")
    
    def set_normal_trigger(self):
        """The command sets the mode of the trigger.
        
        The oscilloscope enters the wait trigger state and begins to search for 
        trigger signals that meet the conditions. If the trigger signal is satisfied, 
        the running state shows Trig'd, and the interface shows stable waveform. 
        Otherwise, the running state shows Ready, and the interface displays the last 
        triggered waveform (previous trigger) or does not display the waveform (no 
        previous trigger).

        :return: Nothing
        """
        self.write(":TRIGger:MODE NORMal")
    
    def set_auto_trigger(self):
        """The command sets the mode of the trigger.
        
        The oscilloscope begins to search for the trigger signal that meets the 
        conditions. If the trigger signal is satisfied, the running state on the top 
        left corner of the user interface shows Trig'd, and the interface shows stable 
        waveform. Otherwise, the running state always shows Auto, and the interface 
        shows unstable waveform.

        :return: Nothing
        """
        self.write(":TRIGger:MODE AUTO")
    
    def set_force_trigger(self):
        """The command sets the mode of the trigger.
        
        Force to acquire a frame regardless of whether the input signal meets the 
        trigger conditions or not.

        :return: Nothing
        """
        self.write(":TRIGger:MODE FTRIG")
    
    def get_trigger_mode(self):
        """The query returns the current mode of trigger.

        :return: str
                    Returns either "SINGle", "NORMal", "AUTO", "FTRIG"
        """
        return self.query(":TRIGger:MODE?")

    def channel_visibile(self, channel : int, visible : bool = True):
        """The command is used to whether display the waveform of the specified 
        channel or not.

        :param channel: 1 to (# analog channels)
        :param visible: Diplay state, defaults to True
        """
        assert 1 <= channel <= 4    # probably need to change to specific 
                                    # oscope

        visible = "ON" if visible else "OFF"

        self.write(":CHANnel{}:VISible {}".format(str(channel), visible))

    def is_channel_visible(self, channel : int):
        """The query returns whether the waveform display function of the selected 
        channel is on or off.

        :param channel: 1 to (# analog channels)
        :return: bool
        """
        assert 1 <= channel <= 4    # probably need to change to specific 
                                    # oscope

        resp = self.query("CHAN{}:VIS?".format(str(channel)))
                          
        return ( True if resp == "ON" else False )
        
    def set_waveform_format_width(self, waveform_width : SiglentWaveformWidth):
        """The command sets the current output format for the transfer of waveform
        data.

        :param waveform_width:  SiglentWaveformWidth.BYTE or SiglentWaveformWidth.WORD
        """
        assert isinstance(waveform_width, SiglentWaveformWidth)

        self.write(":WAVeform:WIDTh {}".format(waveform_width.value))

    def get_waveform_format_width(self) -> SiglentWaveformWidth:
        """The query returns the current output format for the transfer of waveform 
        data.
        """
        resp = self.query(":WAVeform:WIDTh?")

        match resp:
            case "BYTE":
                return SiglentWaveformWidth.BYTE
            case "WORD":
                return SiglentWaveformWidth.WORD

    def arm(self):
        '''Sets up the acquisition signal to single
        '''
        self.set_single_trigger()


    def default_setup(self):
        pass