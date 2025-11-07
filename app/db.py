import sqlite3
import os

# Verbindung zur SQLite-Datenbank herstellen
def verbindung_herstellen():
    # Pfad zur Datenbankdatei im gleichen Ordner wie dieses Skript
    db_pfad = os.path.join(os.path.dirname(__file__), "app.db")
    verbindung = sqlite3.connect(db_pfad)
    verbindung.row_factory = sqlite3.Row
    return verbindung


# Datenbank initialisieren – Tabellen anlegen, falls sie noch nicht existieren
def datenbank_initialisieren():
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    # Tabelle für Kunden
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kunden (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            telefon TEXT,
            adresse TEXT
        )
    """)

    # Tabelle für Aufträge (mit Verknüpfung zu Kunde)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auftraege (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kunde_id INTEGER NOT NULL,
            beschreibung TEXT,
            betrag REAL,
            datum TEXT,
            FOREIGN KEY (kunde_id) REFERENCES kunden(id)
        )
    """)

    verbindung.commit()
    verbindung.close()
    print("✅ Datenbank erfolgreich initialisiert.")
