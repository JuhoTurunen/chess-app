import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()

    def test_konstruktori_luo_kassapaatteen_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)


    def test_kateinen_syo_edullisesti_kasvattaa_rahamaaraa(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(241), 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1002.4)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_kateinen_syo_edullisesti_ei_kasvatta_rahamaaraa_jos_ei_riita(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(239), 239)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_kateinen_syo_maukkaasti_kasvattaa_rahamaaraa(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(401), 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1004.0)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_kateinen_syo_maukkaasti_ei_kasvatta_rahamaaraa_jos_ei_riita(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(399), 399)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        

    def test_kortti_syo_edullisesti_kasvattaa_rahamaaraa(self):
        maksukortti = Maksukortti(241)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(maksukortti), True)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(maksukortti.saldo, 1)

    def test_kortti_syo_edullisesti_ei_kasvatta_rahamaaraa_jos_ei_riita(self):
        maksukortti = Maksukortti(239)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(maksukortti), False)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(maksukortti.saldo, 239)

    def test_kortti_syo_maukkaasti_kasvattaa_rahamaaraa(self):
        maksukortti = Maksukortti(401)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(maksukortti), True)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(maksukortti.saldo, 1)

    def test_kortti_syo_maukkaasti_ei_kasvatta_rahamaaraa_jos_ei_riita(self):
        maksukortti = Maksukortti(399)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(maksukortti), False)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(maksukortti.saldo, 399)


    def test_lataa_rahaa_kortille(self):
        maksukortti = Maksukortti(400)
        self.kassapaate.lataa_rahaa_kortille(maksukortti, 200)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1002.0)
        self.assertEqual(maksukortti.saldo, 600)
    
    def test_lataa_negatiivista_rahaa_kortille_ei_toimi(self):
        maksukortti = Maksukortti(400)
        self.kassapaate.lataa_rahaa_kortille(maksukortti, -200)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)
        self.assertEqual(maksukortti.saldo, 400)