import re

# ------------------------------------------------------------
# EINGABEPROFEN FÜR KUNDEN
# ------------------------------------------------------------

def pruefe_kunde(name, email, telefon, adresse):
    fehler = []

    # Name darf nicht leer sein
    if not name or name.strip() == "":
        fehler.append("Der Name darf nicht leer sein.")

    # E-Mail darf nicht leer sein und muss ein einfaches Format haben
    if not email or email.strip() == "":
        fehler.append("Die E-Mail darf nicht leer sein.")
    else:
        # einfache E-Mail-Prüfung mit Regex
        muster = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(muster, email):
            fehler.append("Bitte eine gültige E-Mail-Adresse eingeben.")

    # Telefonnummer darf leer sein, aber wenn vorhanden, muss sie Zahlen enthalten
    if telefon and not re.match(r"^[0-9\+\-\s]+$", telefon):
        fehler.append("Telefonnummer darf nur Ziffern, +, - oder Leerzeichen enthalten.")

    # Adresse darf nicht leer sein
    if not adresse or adresse.strip() == "":
        fehler.append("Die Adresse darf nicht leer sein.")

    return fehler


# ------------------------------------------------------------
# EINGABEPROFEN FÜR AUFTRÄGE
# ------------------------------------------------------------

def pruefe_auftrag(kunde_id, beschreibung, betrag, datum):
    fehler = []

    # Prüfen, ob Kunde gewählt wurde
    if not kunde_id or kunde_id == "0":
        fehler.append("Bitte wähle einen Kunden aus.")

    # Beschreibung darf nicht leer sein
    if not beschreibung:
        fehler.append("Die Auftragsbeschreibung darf nicht leer sein.")

    # Betrag muss Zahl sein
    try:
        betrag_float = float(betrag)
        if betrag_float <= 0:
            fehler.append("Der Betrag muss größer als 0 sein.")
    except ValueError:
        fehler.append("Der Betrag muss eine Zahl sein.")

    # Datum prüfen (Format grob)
    if not datum:
        fehler.append("Bitte gib ein Auftragsdatum an.")
    elif len(datum) < 8:
        fehler.append("Ungültiges Datum.")

    return fehler
