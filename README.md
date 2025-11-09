# Kunden- & Auftragsverwaltungssystem (Flask + SQLite)

Ein kleines, verständliches Websystem zum Verwalten von Kunden und Aufträgen – mit Filter, Berichten, CSV-Export, Validierung, UnitTests und einem separaten Microservice (Read-only JSON-API).  
Alle Bezeichner und Kommentare sind auf Deutsch.

---

## Voraussetzungen

- Python 3.x
- pip installiert
- Betrieb: lokal (keine Cloud erforderlich)

---

## Installation

```bash
# Projektverzeichnis wechseln
cd kundensystem

# Abhängigkeiten installieren
pip install -r requirements.txt
```

Tipp (Windows): Falls mehrere Python-Versionen vorhanden sind, ggf.  
`py -m pip install -r requirements.txt`

---

## Datenbank einrichten / migrieren

```bash
python app/setup_db.py
```

- Legt Tabellen an (falls neu).
- Rüstet PLZ (bei Kunden) und Status (bei Aufträgen) sicher nach.
- Ausgabe zeigt die vorhandenen Spalten.

---

## Start (lokal)

**Hauptanwendung (Web-UI):**

```bash
# Variante A (empfohlen)
python -m app.main

# Variante B
python app/main.py
```

Aufruf im Browser:  
[http://127.0.0.1:5000](http://127.0.0.1:5000)

**Microservice (Read-only JSON-API):**

```bash
# Standard-Port 5001
python -m app.microservice
# oder
python app/microservice.py
```

- Übersicht: GET /
- Health: GET /api/health
- Umsatzkennzahlen: GET /api/umsatz
- Status-Bericht: GET /api/status-bericht

Port ändern:

```bash
# Linux/Mac
PORT_MICROSERVICE=5100 python -m app.microservice

# Windows PowerShell
$env:PORT_MICROSERVICE=5100; python -m app.microservice
```

---

## Bedienung

### Kunden

- Anlegen / Bearbeiten / Löschen
- Felder: Name, E-Mail, Telefon, Adresse, PLZ
- Filter oben:
  - name (Teiltreffer)
  - plz (genau)

### Aufträge

- Anlegen / Bearbeiten / Löschen
- Felder: Kunde (Dropdown), Beschreibung, Betrag, Datum, Status (offen/erledigt)
- Filter oben:
  - status (offen/erledigt)

### Berichte

- Gesamtumsatz (SUM)
- Durchschnittlicher Auftragswert (AVG)
- Umsatz pro Kunde (GROUP BY)
- Aufträge nach Status: Anzahl & Summe für offen und erledigt

### CSV-Export

- Kunden → Spalten: ID;Name;E-Mail;Telefon;Adresse;PLZ
- Aufträge → Spalten: ID;Kunde;Beschreibung;Betrag;Datum;Status
- Kodierung: UTF-8, Trennzeichen: Semikolon (;)
- Seite: /export → Download-Links

---

## Validierung (Eingabeprüfung)

**Kunde**

- Name/Adresse: nicht leer
- E-Mail: einfaches Format name@domain.tld
- Telefon: nur Ziffern, +, -, Leerzeichen
- PLZ: genau 5 Ziffern

**Auftrag**

- Beschreibung: nicht leer
- Betrag: Zahl ≥ 0
- Datum: nicht leer
- Status: offen oder erledigt

Fehler werden als Liste oberhalb der Formulare angezeigt.

---

## Tests

```bash
python -m unittest -v
```

Enthaltene Tests:

- DB-Verbindung
- Validierung (E-Mail/PLZ/Betrag/Status)
- Filter (Kunden: Name/PLZ · Aufträge: Status)
- Status-Bericht (offen/erledigt: Anzahl & Summe)

Tests nutzen die echte app.db, legen Testdaten mit Präfix TEST_ an und räumen selbst auf.

---

## Projektstruktur

```
app/
├─ __init__.py
├─ main.py            # Flask-UI (Routen, Seiten)
├─ microservice.py    # Getrennter Read-only JSON-Microservice
├─ db.py              # DB-Verbindung + Initialisierung/Migration
├─ speicher.py        # CRUD + Filter (Kunden/Aufträge)
├─ pruefung.py        # Eingabeprüfungen
├─ berichte.py        # SQL-Auswertungen (SUM/AVG/Status)
├─ export.py          # CSV-Export
├─ setup_db.py        # DB-Setup/Migration ausführen
├─ templates/
│  ├─ base.html
│  ├─ index.html
│  ├─ kunden.html
│  ├─ kunde_bearbeiten.html
│  ├─ auftraege.html
│  ├─ auftrag_bearbeiten.html
│  ├─ berichte.html
│  └─ export.html
├─ static/
│  └─ style.css
└─ tests/
   └─ test_app.py
```

---

## Abgrenzung (bewusst einfach gehalten)

- Kein Login/Rechtemanagement
- Keine Rechnungs-/Zahlungsprozesse
- Keine E-Mail-Integration
- Kein Cloud-Zwang – lokaler Betrieb reicht aus

---

## Troubleshooting

**Fehler:** `ModuleNotFoundError: No module named 'speicher'`  
Lösung: App als Modul starten → `python -m app.main`  
Alternativ funktionieren alle Imports durch den integrierten Fallback.

**Fehler:** 404 im Microservice auf "/"  
Lösung: In der finalen Version vorhanden, liefert eine kleine JSON-Übersicht.

**Problem:** CSV öffnet sich komisch in Excel  
Lösung: Beim Import „Trennzeichen = Semikolon“ wählen, Kodierung UTF-8.

---

## Hinweise für IHK

- Muss-Umfang erfüllt: CRUD (Kunden/Aufträge inkl. Bearbeiten/Löschen), Filter (Name/PLZ/Status), Validierungen, Berichte inkl. Status, CSV-Exporte, UnitTests.
- Einfachheit & Nachvollziehbarkeit: Deutsch kommentiert, modulare Struktur, kleiner Microservice als klar abgegrenzte Zusatzkomponente (Read-only).
- Lokalbetrieb als Standard – kein Cloud-Zwang.
