import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)
    
    
    def test_konstruktori_asettaa_saldon_oikein(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")
        
    def test_kortille_voi_ladata_rahaa(self):
        self.maksukortti.lataa_rahaa(2500)

        self.assertEqual(self.maksukortti.saldo_euroina(), 35.0)
        
    def test_kortilta_voi_ottaa_rahaa(self):
        self.assertEqual(self.maksukortti.ota_rahaa(500), True)
        self.assertEqual(self.maksukortti.saldo_euroina(), 5.0)
    
    def test_kortilta_ei_voi_ottaa_ylimaaraista_rahaa(self):
        self.assertEqual(self.maksukortti.ota_rahaa(1500), False)
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)
