import unittest
from SiglentSDS2000xPlusPy.siglentsds2000xplus import *

HOST = ''

class TestSDS2000X(unittest.TestCase):
    def setUp(self) -> None:
        self.scope = SiglentSDS2000XPlus(HOST)
    
    def tearDown(self) -> None:
        del self.scope

    def test_vendor(self):
        self.assertEqual(self.scope.vendor, 'Siglent Technologies')
        
    def test_product(self):
        sds2000x_list = ['SDS2102X Plus', 'SDS2104X Plus', 'SDS2204X Plus', 'SDS2354X Plus', 'SDS2504X Plus']
        self.assertIn(self.scope.product, sds2000x_list)

    def test_set_single_trigger_mode(self):
        self.scope.set_single_trigger()
        self.assertEqual(self.scope.get_trigger_mode(), 'SINGle')

    def test_set_normal_trigger_mode(self):
        self.scope.set_normal_trigger()
        self.assertEqual(self.scope.get_trigger_mode(), 'NORMal')

    def test_set_auto_trigger_mode(self):
        self.scope.set_auto_trigger()
        self.assertEqual(self.scope.get_trigger_mode(), 'AUTO')

    def test_set_force_trigger_mode(self):
        self.scope.set_force_trigger()
        self.assertEqual(self.scope.get_trigger_mode(), 'FTRIG')
    
    def test_channel_visibility_off(self):
        self.scope.channel_visibile(1, False)
        self.assertEqual(self.scope.is_channel_visible(1), False)

        self.scope.channel_visibile(2, False)
        self.assertEqual(self.scope.is_channel_visible(2), False)
        
        self.scope.channel_visibile(3, False)
        self.assertEqual(self.scope.is_channel_visible(3), False)
        
        self.scope.channel_visibile(4, False)
        self.assertEqual(self.scope.is_channel_visible(4), False)

    def test_channel_visibility_on(self):
        self.scope.channel_visibile(1, True)
        self.assertEqual(self.scope.is_channel_visible(1), True)

        self.scope.channel_visibile(2, True)
        self.assertEqual(self.scope.is_channel_visible(2), True)
        
        self.scope.channel_visibile(3, True)
        self.assertEqual(self.scope.is_channel_visible(3), True)
        
        self.scope.channel_visibile(4, True)
        self.assertEqual(self.scope.is_channel_visible(4), True)

    def test_channel_visibility_out_of_range(self):
        with self.assertRaises(AssertionError):
            self.scope.channel_visibile(0, True)
        
        with self.assertRaises(AssertionError):
            self.scope.channel_visibile(5, True)

        with self.assertRaises(TypeError):
            self.scope.channel_visibile("c1", True)

    def test_waveform_format_width(self):
        self.scope.set_waveform_format_width(SiglentWaveformWidth.WORD)
        self.assertEqual(self.scope.get_waveform_format_width().value, "WORD")
    
        self.scope.set_waveform_format_width(SiglentWaveformWidth.BYTE)
        self.assertEqual(self.scope.get_waveform_format_width().value, "BYTE")

    def test_capture(self):
        self.scope.arm()
        self.scope.capture(SiglentSDS2000XChannel.C1)
        


if __name__ == '__main__':
    unittest.main()