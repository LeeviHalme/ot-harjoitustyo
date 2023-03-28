import unittest
from maksukortti import Maksukortti


class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_ota_rahaa_liikaa(self):
        tulos = self.maksukortti.ota_rahaa(2000)

        self.assertFalse(tulos)
        self.assertEqual(self.maksukortti.saldo, 1000)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")
