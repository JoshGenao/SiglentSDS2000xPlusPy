import time
import vxi11
import struct
import numpy as np
from enum import Enum

class SiglentSDS2000XChannel(Enum):
    C1 = "C1"
    C2 = "C2"
    C3 = "C3"
    C4 = "C4"

class SiglentSDSTriggerStatus(Enum):
    ARM = "Arm"
    READY = "Ready"
    AUTO = "Auto"
    TRIGD = "Trig'd"
    STOP = "Stop"
    ROLL = "Roll"

class SiglentWaveformWidth(Enum):
    BYTE = "BYTE"
    WORD = "WORD"


class SiglentSDS2000XPlus(vxi11.Instrument):
    _name = "Siglent SDS2000X Plus"
    center_code = 127
    full_code = 256

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
    
    def query_raw(self, message, *args, **kwargs):
        """
        Write a message to the scope and read a (binary) answer.

        This is the slightly modified version of :py:meth:`vxi11.Instrument.ask_raw()`.
        It takes a command message string and returns the answer as bytes.

        :param str message: The SCPI command to send to the scope.
        :return: Data read from the device
        """
        data = message.encode('utf-8')
        return self.ask_raw(data, *args, **kwargs)
    
    @property
    def idn(self):
        """The command query identifies the instrument type and software version. The 
        response consists of four different fields providing information on the 
        manufacturer, the scope model, the serial number and the firmware revision.

        :return: Siglent Technologies,<model>,<serial_number>,<firmware>
        """
        return self.query("*IDN?")
    
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
    
    def get_trigger_status(self):
        """The command query returns the current state of the trigger.

        :return: str
                    Returns either "Arm", "Ready", "Auto", "Trig'd", "Stop", "Roll"
        """
        return self.query(":TRIGger:STATus?")
    
    def get_waveform_preamble(self):
        """The query returns the parameters of the source using by the command 
        :WAVeform:SOURce.
        """
        params = self.query_raw(":WAVeform:PREamble?")
        params = params[11:]
        total_points = struct.unpack('i', params[116:120])[0]
        probe = struct.unpack('f', params[328:332])[0]
        vdiv = struct.unpack('f', params[156:160])[0] * probe
        voffset = struct.unpack('f', params[160:164])[0] * probe
        code_per_div = struct.unpack('f', params[164:168])[0] * probe
        timebase = struct.unpack('h', params[324:326])[0]
        delay = struct.unpack('d', params[180:188])[0]
        interval = struct.unpack('f', params[176:180])[0]

        return (total_points, vdiv, voffset, code_per_div, timebase, delay, interval, delay)

    
    def autosetup(self):
        """ This command attempts to automatically adjust the trigger, vertical, and 
        horizontal controls of the oscilloscope to deliver a usable display of the 
        input signal. Autoset is not recommended for use on low frequency events 
        (< 100 Hz).

        :return: Nothing
        """
        self.write(":AUToset")

    def set_trigger_run(self):
        """The command sets the oscilloscope to run
        """
        self.write(":TRIGger:RUN")
    
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
    
    def set_rising_edge_trigger(self):
        """The command sets the slope of the slope trigger to Rising Edge

        :return: Nothing
        """
        self.write(":TRIGger:SLOPe:SLOPe RISing")

    def set_falling_edge_trigger(self):
        """The command sets the slope of the slope trigger to Falling Edge

        :return: Nothing
        """
        self.write(":TRIGger:SLOPe:SLOPe FALLing")

    def set_alternate_edge_trigger(self):
        """The command sets the slope of the slope trigger to Falling Edge

        :return: Nothing
        """
        self.write(":TRIGger:SLOPe:SLOPe ALTernate")

    def get_edge_trigger(self):
        """The query returns the current slope of the slope trigger

        :return: str
                    Returns either "RISing", "FALLing", "ALTernate"
        """
        return self.query(":TRIGger:SLOPe:SLOPe?")

    def set_trigger_source(self, trig_channel: SiglentSDS2000XChannel):
        """The query returns the current trigger source of the slope trigger

        :param trig_channel: Trigger source
        """
        self.write(":TRIGger:SLOPe:SOURce {}".format(trig_channel.value))

    def set_trigger_edge_level(self, level : float):
        """The command sets the trigger level of the edge trigger

        :param level: Trigger level
        """

        """
        TODO: trigger level needs to be between:
        [-4.1*vertical_scale-vertical_offset, 4.1*vertical_scale-vertical_offset]
        """
        self.write(":TRIGger:EDGE:LEVel {}".format(str(level)))

    def save_setup(self, file_location : str):
        """This command saves the current settings to internal or external memory 
        locations.

        Users can recall from local,net storage or U-disk according to requirements

        :param file_location: string of path with an extension “.xml”. 
        """
        if file_location.endswith(".xml"):
            self.write(':SAVE:SETup EXTernal,”{}”'.format(file_location))
        else:
            raise ValueError("Add in string that contains .xml")


    def recall_setup(self, file_location : str):
        """This command will recall the saved settings file from external sources.
        
        Users can recall from local,net storage or U-disk according to requirements

        :param file_location: string of path with an extension “.xml”. 
        """
        if file_location.endswith(".xml"):
            self.write(':RECall:SETup EXTernal,”{}”'.format(file_location))
        else:
            raise ValueError("Add in string that contains .xml")


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
            
    def calculate_voltage(self, x, vdiv, voffset, code_per_div):
        if x > self.center_code:
            x -= self.full_code

        return x * (vdiv/code_per_div) - voffset

    def convert_to_voltage(self, raw_array) -> np.ndarray:
        # Get the parameters of the source 
        total_points, vdiv, voffset, code_per_div, timebase, delay, interval, delay = self.get_waveform_preamble()
        vect_voltage = np.vectorize(self.calculate_voltage)

        return vect_voltage(raw_array, vdiv, voffset, code_per_div)

    def arm(self):
        """Sets up the trigger signal to single
        """
        
        self.set_single_trigger()
        self.set_trigger_run()
        self.query("*OPC?")

    def capture(self, src_channel : SiglentSDS2000XChannel):
        """_summary_

        :param src_channel: _description_
        """
        while True:
            res = self.get_trigger_status()
            if res == SiglentSDSTriggerStatus.STOP.value:
                break

        # Send command that specifies the source waveform to be transferred
        self.write(":WAVeform:SOURce {}".format(src_channel.value))
        data = self.query_raw(":WAVeform:DATA?")
        data = data[11:-2]  # eliminate header and remove last two bytes

        try:
            trace = np.frombuffer(data, dtype=np.byte)
            self._last_trace = self.convert_to_voltage(trace)
        except Exception as e:
            print(e)

        return self._last_trace

    def capture_raw(self, src_channel : SiglentSDS2000XChannel):
        """_summary_

        :param src_channel: _description_
        """
        while True:
            res = self.get_trigger_status()
            if res == SiglentSDSTriggerStatus.STOP.value:
                break

        # Send command that specifies the source waveform to be transferred
        self.write(":WAVeform:SOURce {}".format(src_channel.value))
        data = self.query_raw(":WAVeform:DATA?")
        data = data[11:-2]  # eliminate header and remove last two bytes
        try:
            self._last_trace = np.frombuffer(data, dtype=np.byte)
        except Exception as e:
            print(e)

        return self._last_trace
        



    def default_setup(self):
        pass