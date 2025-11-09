# Import-Fallback
try:
    from app.db import verbindung_herstellen
except ImportError:
    from db import verbindung_herstellen

# ------------------------------------------------------------
# Berichte & Auswertungen
# ------------------------------------------------------------

def gesamtumsatz():
    v = verbindung_herstellen()
    c = v.cursor()
    c.execute("SELECT SUM(betrag) AS summe FROM auftraege")
    row = c.fetchone()
    v.close()
    if not row or row["summe"] is None:
        return 0.0
    return round(float(row["summe"]), 2)


def durchschnitt_auftrag():
    v = verbindung_herstellen()
    c = v.cursor()
    c.execute("SELECT AVG(betrag) AS durchschnitt FROM auftraege")
    row = c.fetchone()
    v.close()
    if not row or row["durchschnitt"] is None:
        return 0.0
    return round(float(row["durchschnitt"]), 2)


def umsatz_pro_kunde():
    v = verbindung_herstellen()
    c = v.cursor()
    c.execute("""
        SELECT k.name AS kunde, ROUND(SUM(a.betrag), 2) AS umsatz
        FROM auftraege a
        JOIN kunden k ON a.kunde_id = k.id
        GROUP BY k.name
        ORDER BY umsatz DESC
    """)
    daten = c.fetchall()
    v.close()
    return daten


def status_bericht():
    # Immer beide Status liefern
    v = verbindung_herstellen()
    c = v.cursor()
    c.execute("""
        SELECT status, COUNT(*) AS anzahl, SUM(betrag) AS summe
        FROM auftraege
        GROUP BY status
    """)
    rows = c.fetchall()
    v.close()

    result = {
        "offen":    {"status": "offen",    "anzahl": 0, "summe": 0.0},
        "erledigt": {"status": "erledigt", "anzahl": 0, "summe": 0.0},
    }
    for r in rows:
        st = (r["status"] or "").strip().lower()
        anzahl = int(r["anzahl"]) if r["anzahl"] is not None else 0
        summe = float(r["summe"]) if r["summe"] is not None else 0.0
        if st in result:
            result[st]["anzahl"] = anzahl
            result[st]["summe"] = round(summe, 2)

    return [result["offen"], result["erledigt"]]
