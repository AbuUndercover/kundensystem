# ------------------------------------------------------------
# UnitTests für das Kunden- & Auftragsverwaltungssystem
# Warum: Wir prüfen die wichtigsten Muss-Funktionen stabil und nachvollziehbar.
# Getestet werden:
#  - DB-Verbindung
#  - Validierung (Kunde: E-Mail/PLZ; Auftrag: Betrag/Datum/Status)
#  - Kunden-Filter (Name/PLZ)
#  - Aufträge: Status-Filter + Status-Bericht (offen/erledigt)
# Hinweis: Tests verwenden die echte app.db. Testdaten werden mit Präfix "TEST_"
#          angelegt und vor/nach jedem Test entfernt.
# ------------------------------------------------------------

import unittest
from datetime import datetime

# Import-Fallback: Tests funktionieren bei "python -m unittest" und direkt.
try:
    from app.db import verbindung_herstellen, datenbank_initialisieren, migration_schritt_1
    from app.speicher import (
        kunde_hinzufuegen, kunde_aktualisieren, alle_kunden_holen, kunden_filtern,
        auftrag_hinzufuegen, alle_auftraege_holen, auftraege_filtern
    )
    from app.pruefung import pruefe_kunde, pruefe_auftrag
    from app.berichte import status_bericht
except ImportError:
    from db import verbindung_herstellen, datenbank_initialisieren, migration_schritt_1
    from speicher import (
        kunde_hinzufuegen, kunde_aktualisieren, alle_kunden_holen, kunden_filtern,
        auftrag_hinzufuegen, alle_auftraege_holen, auftraege_filtern
    )
    from pruefung import pruefe_kunde, pruefe_auftrag
    from berichte import status_bericht


# ----------------------------
# Hilfsfunktionen (Cleanup)
# ----------------------------

def _cleanup_testdaten():
    """Entfernt Test-Kunden und Test-Aufträge mit Präfix 'TEST_'."""
    v = verbindung_herstellen()
    c = v.cursor()
    # Aufträge zuerst löschen (FK-Beziehung)
    c.execute("DELETE FROM auftraege WHERE beschreibung LIKE 'TEST_%'")
    c.execute("DELETE FROM kunden WHERE name LIKE 'TEST_%'")
    v.commit()
    v.close()


def _status_dict():
    """Liest den Status-Bericht und liefert ein Dict {'offen': {...}, 'erledigt': {...}}."""
    daten = status_bericht()
    d = {}
    for row in daten:
        d[row["status"]] = {"anzahl": int(row["anzahl"]), "summe": float(row["summe"])}
    # Sicherstellen, dass beide Schlüssel existieren
    for key in ("offen", "erledigt"):
        if key not in d:
            d[key] = {"anzahl": 0, "summe": 0.0}
    return d


class BasisSetup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Tabellen sicherstellen + Migration (PLZ/Status)
        datenbank_initialisieren()
        migration_schritt_1()

    def setUp(self):
        _cleanup_testdaten()

    def tearDown(self):
        _cleanup_testdaten()


# ----------------------------
# DB & Validierung
# ----------------------------

class TestDBUndValidierung(BasisSetup):

    def test_01_db_verbindung(self):
        v = verbindung_herstellen()
        c = v.cursor()
        c.execute("SELECT 1 AS eins")
        row = c.fetchone()
        v.close()
        self.assertEqual(row["eins"], 1, "DB-SELECT sollte 1 liefern")

    def test_02_pruefe_kunde_email_und_plz(self):
        # Ungültige E-Mail + ungültige PLZ
        fehler = pruefe_kunde(
            name="TEST_Max",
            email="falsch",
            telefon="040 123456",
            adresse="Teststraße 1",
            plz="22a45"   # falsch
        )
        self.assertTrue(any("E-Mail" in m for m in fehler))
        self.assertTrue(any("PLZ" in m for m in fehler))

        # Gültige Daten
        fehler = pruefe_kunde(
            name="TEST_Max",
            email="max@test.de",
            telefon="+49 40 123456",
            adresse="Teststraße 1",
            plz="22045"
        )
        self.assertEqual(fehler, [], "Gültige Kundendaten sollten keine Fehler haben")

    def test_03_pruefe_auftrag_status(self):
        # Ungültiger Status
        fehler = pruefe_auftrag(
            beschreibung="TEST_Auftrag ungültiger Status",
            betrag="99.90",
            datum="2025-01-01",
            status="xyz"
        )
        self.assertTrue(any("Status" in m for m in fehler))

        # Gültiger Status + Betrag
        fehler = pruefe_auftrag(
            beschreibung="TEST_Auftrag ok",
            betrag="100.00",
            datum="2025-01-01",
            status="offen"
        )
        self.assertEqual(fehler, [], "Gültiger Auftrag (offen) sollte keine Fehler haben")


# ----------------------------
# Kunden: Speichern & Filtern
# ----------------------------

class TestKunden(BasisSetup):

    def test_04_kunde_speichern_und_filtern(self):
        # Kunde speichern
        kunde_hinzufuegen(
            name="TEST_Max Mustermann",
            email="max@test.de",
            telefon="040 123456",
            adresse="Testweg 1",
            plz="22045"
        )

        # Per Name (Teiltreffer) + PLZ filtern
        treffer = kunden_filtern(name="Max", plz="22045")
        self.assertTrue(any(k["name"] == "TEST_Max Mustermann" for k in treffer),
                        "Gefilterte Liste sollte den TEST-Kunden enthalten")


# ----------------------------
# Aufträge: Filtern & Status-Bericht
# ----------------------------

class TestAuftraege(BasisSetup):

    def test_05_auftrag_anlegen_filtern_und_statusbericht(self):
        # 1) Test-Kunde anlegen
        kunde_hinzufuegen(
            name="TEST_Kunde Auftraege",
            email="kunde@test.de",
            telefon="040 999999",
            adresse="Testallee 5",
            plz="20095"
        )

        # Kunden-ID holen (einfachster Weg: letzter TEST_-Eintrag)
        kunden = [k for k in alle_kunden_holen() if k["name"].startswith("TEST_")]
        self.assertTrue(len(kunden) > 0, "Es sollte mindestens einen TEST_-Kunden geben")
        kunde_id = kunden[-1]["id"]

        # 2) Statuswerte vorher merken
        vorher = _status_dict()
        vorher_offen_anz = vorher["offen"]["anzahl"]
        vorher_offen_sum = vorher["offen"]["summe"]
        vorher_erledigt_anz = vorher["erledigt"]["anzahl"]
        vorher_erledigt_sum = vorher["erledigt"]["summe"]

        # 3) Zwei Test-Aufträge anlegen (offen/erledigt)
        auftrag_hinzufuegen(kunde_id, "TEST_Order1", "100.0", "2025-01-01", "offen")
        auftrag_hinzufuegen(kunde_id, "TEST_Order2", "50.0", "2025-01-02", "erledigt")

        # 4) Status-Filter prüfen (mind. unsere TEST_-Aufträge enthalten)
        offen = auftraege_filtern("offen")
        erledigt = auftraege_filtern("erledigt")
        self.assertTrue(any(a["beschreibung"] == "TEST_Order1" for a in offen),
                        "Status-Filter 'offen' sollte TEST_Order1 enthalten")
        self.assertTrue(any(a["beschreibung"] == "TEST_Order2" for a in erledigt),
                        "Status-Filter 'erledigt' sollte TEST_Order2 enthalten")

        # 5) Status-Bericht muss um unsere beiden Aufträge erhöht sein
        nachher = _status_dict()
        self.assertEqual(nachher["offen"]["anzahl"], vorher_offen_anz + 1)
        self.assertAlmostEqual(nachher["offen"]["summe"], vorher_offen_sum + 100.0, places=2)
        self.assertEqual(nachher["erledigt"]["anzahl"], vorher_erledigt_anz + 1)
        self.assertAlmostEqual(nachher["erledigt"]["summe"], vorher_erledigt_sum + 50.0, places=2)
