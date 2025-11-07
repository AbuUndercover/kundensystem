from app.db import verbindung_herstellen

# ------------------------------------------------------------
# CRUD-FUNKTIONEN FÜR KUNDEN
# ------------------------------------------------------------

def kunde_hinzufuegen(name, email, telefon, adresse):
    # Warum: Fügt einen neuen Kunden in die Datenbank ein
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()
    cursor.execute("""
        INSERT INTO kunden (name, email, telefon, adresse)
        VALUES (?, ?, ?, ?)
    """, (name, email, telefon, adresse))
    verbindung.commit()
    verbindung.close()
    return True


def alle_kunden_holen():
    # Warum: Holt alle Kunden aus der Tabelle
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()
    cursor.execute("SELECT * FROM kunden ORDER BY name")
    daten = cursor.fetchall()
    verbindung.close()
    return daten


def kunde_aktualisieren(kunde_id, name, email, telefon, adresse):
    # Warum: Ändert Kundendaten anhand der ID
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()
    cursor.execute("""
        UPDATE kunden
        SET name = ?, email = ?, telefon = ?, adresse = ?
        WHERE id = ?
    """, (name, email, telefon, adresse, kunde_id))
    verbindung.commit()
    verbindung.close()
    return True


def kunde_loeschen(kunde_id):
    # Warum: Löscht einen Kunden anhand seiner ID
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()
    cursor.execute("DELETE FROM kunden WHERE id = ?", (kunde_id,))
    verbindung.commit()
    verbindung.close()
    return True


# ------------------------------------------------------------
# CRUD-FUNKTIONEN FÜR AUFTRÄGE
# ------------------------------------------------------------

def auftrag_hinzufuegen(kunde_id, beschreibung, betrag, datum):
    # Warum: Fügt einen neuen Auftrag hinzu (Kunde wird über ID verknüpft)
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()
    cursor.execute("""
        INSERT INTO auftraege (kunde_id, beschreibung, betrag, datum)
        VALUES (?, ?, ?, ?)
    """, (kunde_id, beschreibung, betrag, datum))
    verbindung.commit()
    verbindung.close()
    return True


def alle_auftraege_holen():
    # Warum: Holt alle Aufträge mit Kundennamen (JOIN)
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()
    cursor.execute("""
        SELECT a.id, a.beschreibung, a.betrag, a.datum, k.name AS kunde
        FROM auftraege a
        JOIN kunden k ON a.kunde_id = k.id
        ORDER BY a.datum DESC
    """)
    daten = cursor.fetchall()
    verbindung.close()
    return daten


def auftrag_aktualisieren(auftrag_id, beschreibung, betrag, datum):
    # Warum: Ändert einen bestehenden Auftrag
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()
    cursor.execute("""
        UPDATE auftraege
        SET beschreibung = ?, betrag = ?, datum = ?
        WHERE id = ?
    """, (beschreibung, betrag, datum, auftrag_id))
    verbindung.commit()
    verbindung.close()
    return True


def auftrag_loeschen(auftrag_id):
    # Warum: Löscht einen Auftrag anhand seiner ID
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()
    cursor.execute("DELETE FROM auftraege WHERE id = ?", (auftrag_id,))
    verbindung.commit()
    verbindung.close()
    return True
