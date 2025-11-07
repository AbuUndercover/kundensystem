# ------------------------------------------------------------
# Kunden- und Auftragsverwaltungssystem
# Hauptprogramm: Flask-Routen und App-Start
# ------------------------------------------------------------

from flask import Flask, render_template, request, redirect, url_for, send_file

# Eigene Module (immer mit app.-Prefix!)
from app.speicher import (
    alle_kunden_holen,
    kunde_hinzufuegen,
    alle_auftraege_holen,
    auftrag_hinzufuegen,
)
from app.pruefung import pruefe_kunde, pruefe_auftrag
from app.berichte import gesamtumsatz, umsatz_pro_kunde, durchschnitt_auftrag
from app.export import export_kunden_csv, export_auftraege_csv

# ------------------------------------------------------------
# Flask-App erstellen
# ------------------------------------------------------------
app = Flask(__name__)


# ------------------------------------------------------------
# Startseite
# ------------------------------------------------------------
@app.route("/")
def startseite():
    return render_template("index.html")


# ------------------------------------------------------------
# Kundenverwaltung
# ------------------------------------------------------------
@app.route("/kunden", methods=["GET", "POST"])
def kunden():
    meldungen = []
    erfolg = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        telefon = request.form.get("telefon", "").strip()
        adresse = request.form.get("adresse", "").strip()

        meldungen = pruefe_kunde(name, email, telefon, adresse)
        if not meldungen:
            kunde_hinzufuegen(name, email, telefon, adresse)
            erfolg = "Kunde erfolgreich angelegt."

    kundenliste = alle_kunden_holen()
    return render_template("kunden.html", meldungen=meldungen, erfolg=erfolg, kunden=kundenliste)


# ------------------------------------------------------------
# Auftragsverwaltung
# ------------------------------------------------------------
@app.route("/auftraege", methods=["GET", "POST"])
def auftraege():
    meldungen = []
    erfolg = None

    if request.method == "POST":
        kunde_id = request.form.get("kunde_id")
        beschreibung = request.form.get("beschreibung", "").strip()
        betrag = request.form.get("betrag", "").strip()
        datum = request.form.get("datum", "").strip()

        meldungen = pruefe_auftrag(kunde_id, beschreibung, betrag, datum)
        if not meldungen:
            auftrag_hinzufuegen(kunde_id, beschreibung, betrag, datum)
            erfolg = "Auftrag erfolgreich angelegt."

    kundenliste = alle_kunden_holen()
    auftraege_liste = alle_auftraege_holen()
    return render_template(
        "auftraege.html",
        meldungen=meldungen,
        erfolg=erfolg,
        kunden=kundenliste,
        auftraege=auftraege_liste,
    )


# ------------------------------------------------------------
# Berichte
# ------------------------------------------------------------
@app.route("/berichte")
def berichte():
    summe = gesamtumsatz()
    durchschnitt = durchschnitt_auftrag()
    umsaetze = umsatz_pro_kunde()
    return render_template(
        "berichte.html", summe=summe, durchschnitt=durchschnitt, umsaetze=umsaetze
    )


# ------------------------------------------------------------
# CSV-Export
# ------------------------------------------------------------
@app.route("/export")
def export_start():
    return render_template("export.html")


@app.route("/export/kunden")
def export_kunden():
    pfad = export_kunden_csv()
    return send_file(pfad, as_attachment=True)


@app.route("/export/auftraege")
def export_auftraege():
    pfad = export_auftraege_csv()
    return send_file(pfad, as_attachment=True)


# ------------------------------------------------------------
# App-Startpunkt
# ------------------------------------------------------------
if __name__ == "__main__":
    # Nur lokal starten, nicht auf Render
    app.run(host="0.0.0.0", port=5000, debug=True)

