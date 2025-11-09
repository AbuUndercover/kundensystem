# ------------------------------------------------------------
# Microservice (Read-only JSON-API)
# Warum: Kleiner, separater Dienst, der nur lesend auf Daten zugreift
#        und Kennzahlen als JSON bereitstellt.
#        Endpunkte:
#          - GET /               -> kurze Übersicht
#          - GET /api/health
#          - GET /api/umsatz
#          - GET /api/status-bericht
# ------------------------------------------------------------

from flask import Flask, jsonify
import os

# ------------------------------------------------------------
# Import-Fallback (Modulstart/Skriptstart)
# Warum: Damit der Microservice sowohl mit "python -m app.microservice"
#        als auch mit "python app/microservice.py" gestartet werden kann.
# ------------------------------------------------------------
try:
    from app.berichte import gesamtumsatz, durchschnitt_auftrag, status_bericht
except ImportError:
    from berichte import gesamtumsatz, durchschnitt_auftrag, status_bericht


# ------------------------------------------------------------
# Flask-App erstellen
# ------------------------------------------------------------
app = Flask(__name__)


# ------------------------------------------------------------
# Startseite (Info)
# Warum: Zeigt eine kleine Übersicht mit allen verfügbaren API-Endpunkten.
#        So gibt es keinen 404-Fehler mehr, wenn "/" aufgerufen wird.
# ------------------------------------------------------------
@app.get("/")
def api_root():
    return jsonify({
        "service": "kundensystem-microservice",
        "endpoints": [
            "/api/health",
            "/api/umsatz",
            "/api/status-bericht"
        ]
    }), 200


# ------------------------------------------------------------
# Health-Check
# Warum: Schneller Check, ob der Microservice läuft
# ------------------------------------------------------------
@app.get("/api/health")
def api_health():
    return jsonify({"status": "ok"}), 200


# ------------------------------------------------------------
# Umsatz-Kennzahlen
# Warum: Gesamt- und Durchschnittsumsatz als JSON zurückgeben
# ------------------------------------------------------------
@app.get("/api/umsatz")
def api_umsatz():
    try:
        gesamt = gesamtumsatz()
        durchschnitt = durchschnitt_auftrag()
        return jsonify({
            "gesamt": gesamt,
            "durchschnitt": durchschnitt
        }), 200
    except Exception:
        # Warum: Einfache Fehlermeldung, falls etwas schiefläuft
        return jsonify({"error": "Berechnung fehlgeschlagen"}), 500


# ------------------------------------------------------------
# Aufträge nach Status (offen/erledigt)
# Warum: Berichtsdaten als JSON (Anzahl + Summe je Status)
# ------------------------------------------------------------
@app.get("/api/status-bericht")
def api_status_bericht():
    try:
        daten = status_bericht()
        return jsonify(daten), 200
    except Exception:
        return jsonify({"error": "Abfrage fehlgeschlagen"}), 500


# ------------------------------------------------------------
# App-Start
# Warum: Separater Port für den Microservice, damit er parallel zur Haupt-App läuft.
# ------------------------------------------------------------
if __name__ == "__main__":
    # Hinweis: Port kann per Umgebungsvariable gesetzt werden (z. B. 5001)
    port = int(os.environ.get("PORT_MICROSERVICE", 5001))
    app.run(host="0.0.0.0", port=port)
