import unittest
from varasto import Varasto, InvalidTilavuus


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_konstruktori_negatiivinen_tilavuus(self):
        with self.assertRaises(InvalidTilavuus):
            Varasto(-10)

    def test_konstruktori_taysi_varasto(self):
        self.assertAlmostEqual(Varasto(10, alku_saldo=15).saldo, 10)

    def test_konstruktori_negatiivinen_saldo(self):
        self.assertAlmostEqual(Varasto(10, alku_saldo=-7).saldo, 0)

    def test_lisays_lisaa_negatiivista_saldoa(self):
        self.varasto.lisaa_varastoon(-1)

        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_lisays_lisaa_liikaa_saldoa(self):
        self.varasto.lisaa_varastoon(261)

        self.assertAlmostEqual(self.varasto.saldo, 10)

    def test_lisays_ota_varastosta_liikaa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.ota_varastosta(12), 8)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_lisays_ota_varastosta_negatiivinen_maara(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.ota_varastosta(-5), 0)
        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_str(self):
        self.varasto.lisaa_varastoon(4)

        self.assertEqual(str(self.varasto), "saldo = 4, vielä tilaa 6")
