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
        self.assertEqual(self.scope.product, 'SDS2504X Plus')


if __name__ == '__main__':
    unittest.main()