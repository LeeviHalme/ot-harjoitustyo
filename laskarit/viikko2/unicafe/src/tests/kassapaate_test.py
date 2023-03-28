import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti


class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.paate = Kassapaate()

    def test_constructor(self):
        self.assertEqual(self.paate.kassassa_rahaa, 100000)
        self.assertEqual(self.paate.edulliset, 0)
        self.assertEqual(self.paate.maukkaat, 0)

    def test_kateisosto_riittava_maukkaasti(self):
        vaihto = self.paate.syo_maukkaasti_kateisella(1000)

        self.assertEqual(vaihto, 600)
        self.assertEqual(self.paate.maukkaat, 1)
        self.assertEqual(self.paate.kassassa_rahaa, 100400)

    def test_kateisosto_riittava_edullisesti(self):
        vaihto = self.paate.syo_edullisesti_kateisella(1000)

        self.assertEqual(vaihto, 760)
        self.assertEqual(self.paate.edulliset, 1)
        self.assertEqual(self.paate.kassassa_rahaa, 100240)

    def test_kateisosto_ei_riittava_maukkaasti(self):
        vaihto = self.paate.syo_maukkaasti_kateisella(200)

        self.assertEqual(vaihto, 200)
        self.assertEqual(self.paate.maukkaat, 0)
        self.assertEqual(self.paate.kassassa_rahaa, 100000)

    def test_kateisosto_ei_riittava_edullisesti(self):
        vaihto = self.paate.syo_edullisesti_kateisella(200)

        self.assertEqual(vaihto, 200)
        self.assertEqual(self.paate.edulliset, 0)
        self.assertEqual(self.paate.kassassa_rahaa, 100000)

    def test_korttiosto_riittava_maukkaasti(self):
        kortti = Maksukortti(1000)
        success = self.paate.syo_maukkaasti_kortilla(kortti)

        self.assertTrue(success)
        self.assertEqual(kortti.saldo, 600)
        self.assertEqual(self.paate.maukkaat, 1)
        self.assertEqual(self.paate.kassassa_rahaa, 100000)

    def test_korttiosto_riittava_edullisesti(self):
        kortti = Maksukortti(1000)
        success = self.paate.syo_edullisesti_kortilla(kortti)

        self.assertTrue(success)
        self.assertEqual(kortti.saldo, 760)
        self.assertEqual(self.paate.edulliset, 1)
        self.assertEqual(self.paate.kassassa_rahaa, 100000)

    def test_korttiosto_ei_riittava_maukkaasti(self):
        kortti = Maksukortti(200)
        success = self.paate.syo_maukkaasti_kortilla(kortti)

        self.assertFalse(success)
        self.assertEqual(kortti.saldo, 200)
        self.assertEqual(self.paate.maukkaat, 0)
        self.assertEqual(self.paate.kassassa_rahaa, 100000)

    def test_korttiosto_ei_riittava_edullisesti(self):
        kortti = Maksukortti(200)
        success = self.paate.syo_edullisesti_kortilla(kortti)

        self.assertFalse(success)
        self.assertEqual(kortti.saldo, 200)
        self.assertEqual(self.paate.edulliset, 0)
        self.assertEqual(self.paate.kassassa_rahaa, 100000)

    def test_kortin_lataus(self):
        kortti = Maksukortti(0)
        self.paate.lataa_rahaa_kortille(kortti, 1000)

        self.assertEqual(kortti.saldo, 1000)
        self.assertEqual(self.paate.kassassa_rahaa, 101000)

    def test_kortin_lataus_negatiiviseksi(self):
        kortti = Maksukortti(0)
        success = self.paate.lataa_rahaa_kortille(kortti, -1000)

        self.assertEqual(success, None)
        self.assertEqual(kortti.saldo, 0)
        self.assertEqual(self.paate.kassassa_rahaa, 100000)
