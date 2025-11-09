import re

# ------------------------------------------------------------
# Eingabeprüfungen (Validierung)
# Warum: Wir prüfen Eingaben, bevor sie gespeichert werden,
#        damit keine fehlerhaften Daten in die Datenbank kommen.
# ------------------------------------------------------------

def pruefe_kunde(name, email, telefon, adresse, plz=None):
    fehler = []

    # Name darf nicht leer sein
    if not name or name.strip() == "":
        fehler.append("Der Name darf nicht leer sein.")

    # E-Mail darf nicht leer sein und muss ein einfaches Format haben
    if not email or email.strip() == "":
        fehler.append("Die E-Mail darf nicht leer sein.")
    else:
        # Einfache E-Mail-Prüfung
        muster = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(muster, email):
            fehler.append("Bitte eine gültige E-Mail-Adresse eingeben.")

    # Telefonnummer: optional; wenn vorhanden, nur Ziffern, +, -, Leerzeichen
    if telefon and not re.match(r"^[0-9+\-\s]+$", telefon):
        fehler.append("Telefonnummer darf nur Ziffern, +, - oder Leerzeichen enthalten.")

    # Adresse darf nicht leer sein
    if not adresse or adresse.strip() == "":
        fehler.append("Die Adresse darf nicht leer sein.")

    # PLZ (Schritt 2: optional prüfen; in Schritt 3 wird sie im Formular eingeführt)
    if plz is not None and plz.strip() != "":
        if not re.match(r"^\d{5}$", plz.strip()):
            fehler.append("Die PLZ muss aus genau 5 Ziffern bestehen.")

    return fehler


def pruefe_auftrag(beschreibung, betrag, datum, status=None):
    fehler = []

    # Beschreibung darf nicht leer sein
    if not beschreibung or beschreibung.strip() == "":
        fehler.append("Die Beschreibung darf nicht leer sein.")

    # Betrag muss Zahl >= 0 sein
    try:
        betrag = float(betrag)
        if betrag < 0:
            fehler.append("Der Betrag darf nicht negativ sein.")
    except (ValueError, TypeError):
        fehler.append("Der Betrag muss eine Zahl sein.")

    # Datum darf nicht leer sein
    if not datum or datum.strip() == "":
        fehler.append("Das Datum darf nicht leer sein.")

    # Status (Schritt 2: optional; in Schritt 3 kommt das Feld ins Formular)
    if status is not None and str(status).strip() != "":
        if status not in ("offen", "erledigt"):
            fehler.append("Der Status muss 'offen' oder 'erledigt' sein.")

    return fehler
