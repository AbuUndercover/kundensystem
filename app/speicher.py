# Import-Fallback: funktioniert beim Paketstart (app.*) und Skriptstart
try:
    from app.db import verbindung_herstellen
except ImportError:
    from db import verbindung_herstellen

# ------------------------------------------------------------
# CRUD-FUNKTIONEN FÜR KUNDEN
# ------------------------------------------------------------

def kunde_hinzufuegen(name, email, telefon, adresse, plz):
    # Warum: Fügt einen neuen Kunden in die Datenbank ein (inkl. PLZ)
    v = verbindung_herstellen()
    c = v.cursor()
    c.execute("""
        INSERT INTO kunden (name, email, telefon, adresse, plz)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, telefon, adresse, plz))
    v.commit()
    v.close()
    return True


def alle_kunden_holen():
    # Warum: Holt alle Kunden aus der Tabelle
    v = verbindung_herstellen()
    c = v.cursor()
    c.execute("SELECT * FROM kunden ORDER BY name")
    daten = c.fetchall()
    v.close()
    return daten


def kunden_filtern(name=None, plz=None):
    # Warum: Kunden nach Name (LIKE) und/oder PLZ (=) filtern
    v = verbindung_herstellen()
    c = v.cursor()

    sql = "SELECT * FROM kunden"
    bedingungen, werte = [], []

    if name is not None and name.strip() != "":
        bedingungen.append("name LIKE ?")
        werte.append("%" + name.strip() + "%")

    if plz is not None and plz.strip() != "":
        bedingungen.append("plz = ?")
        werte.append(plz.strip())

    if bedingungen:
        sql += " WHERE " + " AND ".join(bedingungen)

    sql += " ORDER BY name"

    c.execute(sql, tuple(werte))
    daten = c.fetchall()
    v.close()
    return daten


def kunde_aktualisieren(kunde_id, name, email, telefon, adresse, plz):
    # Warum: Ändert Kundendaten anhand der ID (inkl. PLZ)
    v = verbindung_herstellen()
    c = v.cursor()
    c.execute("""
        UPDATE kunden
        SET name = ?, email = ?, telefon = ?, adresse = ?, plz = ?
        WHERE id = ?
    """, (name, email, telefon, adresse, plz, kunde_id))
    v.commit()
    v.close()
    return True


def kunde_loeschen(kunde_id):
    # Warum: Löscht einen Kunden anhand seiner ID
    v = verbindung_herstellen()
    c = v.cursor()
    c.execute("DELETE FROM kunden WHERE id = ?", (kunde_id,))
    v.commit()
    v.close()
    return True


# ------------------------------------------------------------
# CRUD-FUNKTIONEN FÜR AUFTRÄGE
# ------------------------------------------------------------

def auftrag_hinzufuegen(kunde_id, beschreibung, betrag, datum, status):
    # Warum: Fügt einen neuen Auftrag hinzu (inkl. Status)
    v = verbindung_herstellen()
    c = v.cursor()
    c.execute("""
        INSERT INTO auftraege (kunde_id, beschreibung, betrag, datum, status)
        VALUES (?, ?, ?, ?, ?)
    """, (kunde_id, beschreibung, betrag, datum, status))
    v.commit()
    v.close()
    return True


def alle_auftraege_holen():
    # Warum: Holt alle Aufträge mit Kundennamen (JOIN) inkl. Status
    v = verbindung_herstellen()
    c = v.cursor()
    c.execute("""
        SELECT a.id, a.kunde_id, a.beschreibung, a.betrag, a.datum, a.status, k.name AS kunde
        FROM auftraege a
        JOIN kunden k ON a.kunde_id = k.id
        ORDER BY a.datum DESC, a.id DESC
    """)
    daten = c.fetchall()
    v.close()
    return daten


def auftraege_filtern(status=None):
    # Warum: Aufträge nach Status (offen/erledigt) filtern
    v = verbindung_herstellen()
    c = v.cursor()

    sql = """
        SELECT a.id, a.kunde_id, a.beschreibung, a.betrag, a.datum, a.status, k.name AS kunde
        FROM auftraege a
        JOIN kunden k ON a.kunde_id = k.id
    """
    werte = []

    if status is not None and status.strip() != "":
        sql += " WHERE a.status = ?"
        werte.append(status.strip())

    sql += " ORDER BY a.datum DESC, a.id DESC"

    c.execute(sql, tuple(werte))
    daten = c.fetchall()
    v.close()
    return daten


def auftrag_lesen(auftrag_id):
    # Warum: Einzelnen Auftrag für das Bearbeiten-Formular laden (inkl. Kunde)
    v = verbindung_herstellen()
    c = v.cursor()
    c.execute("""
        SELECT a.id, a.kunde_id, a.beschreibung, a.betrag, a.datum, a.status, k.name AS kunde
        FROM auftraege a
        JOIN kunden k ON a.kunde_id = k.id
        WHERE a.id = ?
    """, (auftrag_id,))
    row = c.fetchone()
    v.close()
    return row


def auftrag_aktualisieren(auftrag_id, kunde_id, beschreibung, betrag, datum, status):
    # Warum: Auftrag mit neuen Werten speichern (inkl. Status/Kunde)
    v = verbindung_herstellen()
    c = v.cursor()
    c.execute("""
        UPDATE auftraege
        SET kunde_id = ?, beschreibung = ?, betrag = ?, datum = ?, status = ?
        WHERE id = ?
    """, (kunde_id, beschreibung, betrag, datum, status, auftrag_id))
    v.commit()
    v.close()
    return True


def auftrag_loeschen(auftrag_id):
    # Warum: Löscht einen Auftrag anhand seiner ID
    v = verbindung_herstellen()
    c = v.cursor()
    c.execute("DELETE FROM auftraege WHERE id = ?", (auftrag_id,))
    v.commit()
    v.close()
    return True
