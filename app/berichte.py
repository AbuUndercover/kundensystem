from app.db import verbindung_herstellen

# ------------------------------------------------------------
# Gesamtumsatz berechnen
# ------------------------------------------------------------
def gesamtumsatz():
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()
    cursor.execute("SELECT SUM(betrag) AS summe FROM auftraege")
    ergebnis = cursor.fetchone()
    verbindung.close()
    if ergebnis["summe"] is None:
        return 0.0
    return round(ergebnis["summe"], 2)


# ------------------------------------------------------------
# Umsatz pro Kunde berechnen
# ------------------------------------------------------------
def umsatz_pro_kunde():
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()
    cursor.execute("""
        SELECT k.name AS kunde, SUM(a.betrag) AS umsatz
        FROM auftraege a
        JOIN kunden k ON a.kunde_id = k.id
        GROUP BY k.name
        ORDER BY umsatz DESC
    """)
    daten = cursor.fetchall()
    verbindung.close()
    return daten


# ------------------------------------------------------------
# Durchschnittlicher Auftragswert
# ------------------------------------------------------------
def durchschnitt_auftrag():
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()
    cursor.execute("SELECT AVG(betrag) AS durchschnitt FROM auftraege")
    ergebnis = cursor.fetchone()
    verbindung.close()
    if ergebnis["durchschnitt"] is None:
        return 0.0
    return round(ergebnis["durchschnitt"], 2)
