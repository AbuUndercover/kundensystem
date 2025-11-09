import sqlite3
import os

# Verbindung zur SQLite-Datenbank herstellen
# Warum: Zentrale Stelle für DB-Zugriffe in der ganzen App
def verbindung_herstellen():
    # Datei app.db liegt im gleichen Ordner wie dieses Skript
    db_pfad = os.path.join(os.path.dirname(__file__), "app.db")
    verbindung = sqlite3.connect(db_pfad)
    # Rows als Dictionaries nutzbar machen (einfachere Weiterverarbeitung)
    verbindung.row_factory = sqlite3.Row
    return verbindung


# Datenbank initialisieren – Tabellen anlegen, falls sie noch nicht existieren
# Warum: Beim ersten Start braucht die App die Grundtabellen
def datenbank_initialisieren():
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    # Tabelle für Kunden (mit PLZ-Feld)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kunden (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            telefon TEXT,
            adresse TEXT,
            plz TEXT
        )
    """)

    # Tabelle für Aufträge (mit Status-Feld)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auftraege (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kunde_id INTEGER NOT NULL,
            beschreibung TEXT,
            betrag REAL,
            datum TEXT,
            status TEXT DEFAULT 'offen',
            FOREIGN KEY (kunde_id) REFERENCES kunden(id)
        )
    """)

    verbindung.commit()
    verbindung.close()


# Hilfsfunktion: Prüfen, ob eine Spalte in einer Tabelle existiert
# Warum: Bei bestehender DB Spalten gefahrlos nachrüsten, ohne Daten zu verlieren
def _spalte_existiert(cursor, tabelle, spaltenname):
    cursor.execute(f"PRAGMA table_info({tabelle})")
    infos = cursor.fetchall()
    for zeile in infos:
        # zeile["name"] ist der Spaltenname
        if zeile["name"] == spaltenname:
            return True
    return False


# Migration Schritt 1: fehlende Spalten PLZ (kunden) und STATUS (auftraege) ergänzen
# Warum: Bestehende Installationen erhalten neue Felder, ohne dass Daten gelöscht werden
def migration_schritt_1():
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    # Kunden: Spalte plz (TEXT) ergänzen, falls sie fehlt
    if not _spalte_existiert(cursor, "kunden", "plz"):
        cursor.execute("ALTER TABLE kunden ADD COLUMN plz TEXT")
        # Hinweis: ALTER TABLE ergänzt die Spalte mit NULL für bestehende Zeilen

    # Aufträge: Spalte status (TEXT) ergänzen, falls sie fehlt
    if not _spalte_existiert(cursor, "auftraege", "status"):
        cursor.execute("ALTER TABLE auftraege ADD COLUMN status TEXT DEFAULT 'offen'")
        # Bestehende Zeilen erhalten den Default-Wert 'offen' (sofern möglich)

    verbindung.commit()
    verbindung.close()


# Kleiner Selbsttest für die Migration (optional vom Setup aufrufbar)
# Warum: Schnelle Kontrolle, ob die Spalten nun vorhanden sind
def kurztest_spalten():
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    cursor.execute("PRAGMA table_info(kunden)")
    kunden_spalten = [r["name"] for r in cursor.fetchall()]

    cursor.execute("PRAGMA table_info(auftraege)")
    auftrag_spalten = [r["name"] for r in cursor.fetchall()]

    verbindung.close()
    return {
        "kunden": kunden_spalten,
        "auftraege": auftrag_spalten
    }
