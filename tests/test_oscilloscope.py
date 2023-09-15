import unittest
from SiglentSDS2000xPlusPy.siglentsds2000xplus import SiglentSDS2000XPlus

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
    
    def test_waveform_preamble(self):
        pass


if __name__ == '__main__':
    unittest.main()