import csv
import os
from app.db import verbindung_herstellen

# ------------------------------------------------------------
# CSV-Export für Kunden
# ------------------------------------------------------------
def export_kunden_csv(dateiname="kunden_export.csv"):
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()
    cursor.execute("SELECT * FROM kunden")
    daten = cursor.fetchall()
    verbindung.close()

    # Datei im app-Ordner speichern
    pfad = os.path.join(os.path.dirname(__file__), dateiname)
    with open(pfad, "w", newline="", encoding="utf-8") as csv_datei:
        writer = csv.writer(csv_datei, delimiter=";")
        writer.writerow(["ID", "Name", "E-Mail", "Telefon", "Adresse"])
        for zeile in daten:
            writer.writerow([zeile["id"], zeile["name"], zeile["email"], zeile["telefon"], zeile["adresse"]])
    return pfad


# ------------------------------------------------------------
# CSV-Export für Aufträge
# ------------------------------------------------------------
def export_auftraege_csv(dateiname="auftraege_export.csv"):
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()
    cursor.execute("""
        SELECT a.id, k.name AS kunde, a.beschreibung, a.betrag, a.datum
        FROM auftraege a
        JOIN kunden k ON a.kunde_id = k.id
        ORDER BY a.datum DESC
    """)
    daten = cursor.fetchall()
    verbindung.close()

    pfad = os.path.join(os.path.dirname(__file__), dateiname)
    with open(pfad, "w", newline="", encoding="utf-8") as csv_datei:
        writer = csv.writer(csv_datei, delimiter=";")
        writer.writerow(["ID", "Kunde", "Beschreibung", "Betrag", "Datum"])
        for zeile in daten:
            writer.writerow([zeile["id"], zeile["kunde"], zeile["beschreibung"], zeile["betrag"], zeile["datum"]])
    return pfad
