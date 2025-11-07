import unittest
import os
from app.db import verbindung_herstellen, datenbank_initialisieren
from app.speicher import kunde_hinzufuegen, alle_kunden_holen
from app.pruefung import pruefe_kunde


class TestApp(unittest.TestCase):
    """Einfache Tests für die IHK-Projektfunktionen"""

    def setUp(self):
        """Vor jedem Test wird eine neue, saubere Test-Datenbank angelegt"""
        if os.path.exists("app/app.db"):
            os.remove("app/app.db")
        datenbank_initialisieren()

    # ----------------------------------------------------------
    # Test 1: Datenbankverbindung
    # ----------------------------------------------------------
    def test_verbindung(self):
        verbindung = verbindung_herstellen()
        self.assertIsNotNone(verbindung)
        verbindung.close()

    # ----------------------------------------------------------
    # Test 2: Kunde speichern und abrufen
    # ----------------------------------------------------------
    def test_kunde_speichern(self):
        kunde_hinzufuegen("Max Mustermann", "max@test.de", "01234", "Teststraße 1")
        kunden = alle_kunden_holen()
        self.assertEqual(len(kunden), 1)
        self.assertEqual(kunden[0]["name"], "Max Mustermann")

    # ----------------------------------------------------------
    # Test 3: Eingabeprüfung
    # ----------------------------------------------------------
    def test_pruefung_kunde(self):
        fehler = pruefe_kunde("", "falsch@", "abc!", "")
        self.assertTrue(len(fehler) > 0)
        korrekt = pruefe_kunde("Max", "max@test.de", "01234", "Adresse 1")
        self.assertEqual(len(korrekt), 0)


if __name__ == "__main__":
    unittest.main()
