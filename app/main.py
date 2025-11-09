# ------------------------------------------------------------
# Kunden- und Auftragsverwaltungssystem
# Hauptprogramm: Flask-Routen und App-Start
# ------------------------------------------------------------

from flask import Flask, render_template, request, redirect, url_for, send_file
import os

# ------------------------------------------------------------
# Import-Fallback (Modulstart/Skriptstart)
# ------------------------------------------------------------
try:
    from app.speicher import (
        alle_kunden_holen,
        kunden_filtern,
        kunde_hinzufuegen,
        kunde_loeschen,
        kunde_aktualisieren,
        alle_auftraege_holen,
        auftraege_filtern,
        auftrag_hinzufuegen,
        auftrag_lesen,
        auftrag_aktualisieren,
        auftrag_loeschen,
    )
    from app.pruefung import pruefe_kunde, pruefe_auftrag
    from app.berichte import gesamtumsatz, umsatz_pro_kunde, durchschnitt_auftrag, status_bericht
    from app.export import export_kunden_csv, export_auftraege_csv
except ImportError:
    from speicher import (
        alle_kunden_holen,
        kunden_filtern,
        kunde_hinzufuegen,
        kunde_loeschen,
        kunde_aktualisieren,
        alle_auftraege_holen,
        auftraege_filtern,
        auftrag_hinzufuegen,
        auftrag_lesen,
        auftrag_aktualisieren,
        auftrag_loeschen,
    )
    from pruefung import pruefe_kunde, pruefe_auftrag
    from berichte import gesamtumsatz, umsatz_pro_kunde, durchschnitt_auftrag, status_bericht
    from export import export_kunden_csv, export_auftraege_csv


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
# Kundenverwaltung + Filter (Name, PLZ)
# ------------------------------------------------------------
@app.route("/kunden", methods=["GET", "POST"])
def kunden():
    meldungen = []
    erfolg = None

    name_q = request.args.get("name", "").strip()
    plz_q = request.args.get("plz", "").strip()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        telefon = request.form.get("telefon", "").strip()
        adresse = request.form.get("adresse", "").strip()
        plz = request.form.get("plz", "").strip()

        meldungen = pruefe_kunde(name, email, telefon, adresse, plz)

        if not meldungen:
            kunde_hinzufuegen(name, email, telefon, adresse, plz)
            erfolg = "Kunde erfolgreich angelegt."

    if name_q != "" or plz_q != "":
        kundenliste = kunden_filtern(name_q, plz_q)
    else:
        kundenliste = alle_kunden_holen()

    return render_template(
        "kunden.html",
        meldungen=meldungen,
        erfolg=erfolg,
        kunden=kundenliste,
        name_q=name_q,
        plz_q=plz_q
    )


# ------------------------------------------------------------
# Kunden löschen
# ------------------------------------------------------------
@app.route("/kunden/loeschen/<int:kunde_id>")
def kunde_loeschen_route(kunde_id):
    kunde_loeschen(kunde_id)
    return redirect(url_for("kunden"))


# ------------------------------------------------------------
# Kunden bearbeiten
# ------------------------------------------------------------
@app.route("/kunden/bearbeiten/<int:kunde_id>", methods=["GET", "POST"])
def kunde_bearbeiten(kunde_id):
    meldungen = []
    erfolg = None

    kunden_liste = alle_kunden_holen()

    aktueller_kunde = None
    for k in kunden_liste:
        if k["id"] == kunde_id:
            aktueller_kunde = k
            break

    if aktueller_kunde is None:
        meldungen.append("Kunde nicht gefunden.")
        return render_template("kunden.html", kunden=kunden_liste, meldungen=meldungen)

    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        telefon = request.form.get("telefon", "")
        adresse = request.form.get("adresse", "")
        plz = request.form.get("plz", "")

        fehler = pruefe_kunde(name, email, telefon, adresse, plz)
        if fehler:
            meldungen = fehler
        else:
            kunde_aktualisieren(kunde_id, name, email, telefon, adresse, plz)
            erfolg = "Kundendaten wurden aktualisiert."
            return redirect(url_for("kunden"))

    return render_template(
        "kunde_bearbeiten.html",
        kunde=aktueller_kunde,
        meldungen=meldungen,
        erfolg=erfolg
    )


# ------------------------------------------------------------
# Auftragsverwaltung + Filter (Status)
# ------------------------------------------------------------
@app.route("/auftraege", methods=["GET", "POST"])
def auftraege():
    meldungen = []
    erfolg = None

    status_q = request.args.get("status", "").strip()

    if request.method == "POST":
        kunde_id = request.form.get("kunde_id")
        beschreibung = request.form.get("beschreibung", "").strip()
        betrag = request.form.get("betrag", "").strip()
        datum = request.form.get("datum", "").strip()
        status = request.form.get("status", "offen").strip() or "offen"

        meldungen = pruefe_auftrag(beschreibung, betrag, datum, status)

        if not meldungen:
            auftrag_hinzufuegen(kunde_id, beschreibung, betrag, datum, status)
            erfolg = "Auftrag erfolgreich angelegt."

    if status_q != "":
        auftraege_liste = auftraege_filtern(status_q)
    else:
        auftraege_liste = alle_auftraege_holen()

    kundenliste = alle_kunden_holen()

    return render_template(
        "auftraege.html",
        meldungen=meldungen,
        erfolg=erfolg,
        kunden=kundenliste,
        auftraege=auftraege_liste,
        status_q=status_q
    )


# ------------------------------------------------------------
# Auftrag bearbeiten (NEU)
# ------------------------------------------------------------
@app.route("/auftraege/bearbeiten/<int:auftrag_id>", methods=["GET", "POST"])
def auftrag_bearbeiten(auftrag_id):
    meldungen = []
    erfolg = None

    # Warum: Kundenliste für Dropdown laden
    kundenliste = alle_kunden_holen()

    # Aktuellen Auftrag laden
    aktueller_auftrag = auftrag_lesen(auftrag_id)
    if aktueller_auftrag is None:
        meldungen.append("Auftrag nicht gefunden.")
        # Zurück zur Liste, wenn ID ungültig
        return redirect(url_for("auftraege"))

    if request.method == "POST":
        kunde_id = request.form.get("kunde_id")
        beschreibung = request.form.get("beschreibung", "").strip()
        betrag = request.form.get("betrag", "").strip()
        datum = request.form.get("datum", "").strip()
        status = request.form.get("status", "offen").strip() or "offen"

        fehler = pruefe_auftrag(beschreibung, betrag, datum, status)
        if fehler:
            meldungen = fehler
        else:
            auftrag_aktualisieren(auftrag_id, kunde_id, beschreibung, betrag, datum, status)
            erfolg = "Auftragsdaten wurden aktualisiert."
            return redirect(url_for("auftraege"))

    return render_template(
        "auftrag_bearbeiten.html",
        auftrag=aktueller_auftrag,
        kunden=kundenliste,
        meldungen=meldungen,
        erfolg=erfolg
    )


# ------------------------------------------------------------
# Auftrag löschen
# ------------------------------------------------------------
@app.route("/auftraege/loeschen/<int:auftrag_id>")
def auftrag_loeschen_route(auftrag_id):
    auftrag_loeschen(auftrag_id)
    return redirect(url_for("auftraege"))


# ------------------------------------------------------------
# Berichte (inkl. Status-Übersicht)
# ------------------------------------------------------------
@app.route("/berichte")
def berichte():
    summe = gesamtumsatz()
    durchschnitt = durchschnitt_auftrag()
    umsaetze = umsatz_pro_kunde()
    status_daten = status_bericht()
    return render_template(
        "berichte.html",
        summe=summe,
        durchschnitt=durchschnitt,
        umsaetze=umsaetze,
        status_daten=status_daten
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
