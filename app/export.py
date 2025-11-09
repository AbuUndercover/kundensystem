# ------------------------------------------------------------
# CSV-Export: Kunden & Aufträge
# ------------------------------------------------------------
import csv
import os
from datetime import datetime

# Import-Fallback
try:
    from app.db import verbindung_herstellen
except ImportError:
    from db import verbindung_herstellen


def _export_pfad(basis):
    ordner = os.path.dirname(__file__)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(ordner, f"{basis}_{ts}.csv")


def export_kunden_csv():
    pfad = _export_pfad("kunden_export")
    v = verbindung_herstellen()
    c = v.cursor()
    c.execute("""
        SELECT id, name, email, telefon, adresse, plz
        FROM kunden
        ORDER BY name
    """)
    zeilen = c.fetchall()
    v.close()

    with open(pfad, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        w.writerow(["ID", "Name", "E-Mail", "Telefon", "Adresse", "PLZ"])
        for r in zeilen:
            w.writerow([
                r["id"],
                r["name"] or "",
                r["email"] or "",
                r["telefon"] or "",
                r["adresse"] or "",
                r["plz"] or "",
            ])
    return pfad


def export_auftraege_csv():
    pfad = _export_pfad("auftraege_export")
    v = verbindung_herstellen()
    c = v.cursor()
    c.execute("""
        SELECT a.id, k.name AS kunde, a.beschreibung, a.betrag, a.datum, a.status
        FROM auftraege a
        JOIN kunden k ON k.id = a.kunde_id
        ORDER BY a.datum DESC, a.id DESC
    """)
    zeilen = c.fetchall()
    v.close()

    with open(pfad, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        w.writerow(["ID", "Kunde", "Beschreibung", "Betrag", "Datum", "Status"])
        for r in zeilen:
            betrag = "" if r["betrag"] is None else str(r["betrag"])
            w.writerow([
                r["id"],
                r["kunde"] or "",
                r["beschreibung"] or "",
                betrag,
                r["datum"] or "",
                (r["status"] or "").strip() or "offen",
            ])
    return pfad
