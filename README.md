# Kunden- und Auftragsverwaltungssystem

## Projektbeschreibung
Dieses Projekt wurde im Rahmen meines Praktikums bei der GFN GmbH Hamburg während meiner Umschulung zum Fachinformatiker für Anwendungsentwicklung erstellt.  
Ziel war es, eine einfache, funktionsfähige Webanwendung zur Verwaltung von Kunden- und Auftragsdaten zu entwickeln.  
Die Anwendung basiert auf Flask und SQLite und dient als Lern- und Praxisprojekt, um Kenntnisse in Python, Webentwicklung und Datenbankdesign zu vertiefen.

Das System ermöglicht:
- Kunden anlegen, anzeigen und löschen
- Aufträge anlegen und mit Kunden verknüpfen
- Berichte (Gesamtumsatz, Umsatz pro Kunde, Durchschnitt)
- CSV-Export aller Daten
- Eingabeprüfung und einfache UnitTests

## Technologien
Python 3, Flask, SQLite, HTML/CSS, unittest

## Struktur

app/
├── main.py # Hauptprogramm mit allen Flask-Routen
├── db.py # Verbindung und Erstellung der SQLite-Datenbank
├── speicher.py # CRUD-Funktionen für Kunden und Aufträge
├── pruefung.py # Eingabevalidierung für Formulare
├── berichte.py # SQL-Auswertungen und Statistiken
├── export.py # CSV-Export-Funktionen
├── templates/ # HTML-Templates (Jinja2)
├── static/ # CSS-Dateien und statische Inhalte
└── tests/ # UnitTests für zentrale Funktionen


## Installation und Start
```bash
python -m venv .venv
# Windows:

source .venv/bin/activate

pip install flask

# Datenbank initialisieren
python -m app.setup_db

# Anwendung starten
python -m app.main


##Danach im Browser öffnen:
http://127.0.0.1:5000

##Praktischer Nutzen

#Das Projekt wurde im Rahmen eines Praktikums als Lern- und Übungsaufgabe umgesetzt.
#Es diente dazu, den Umgang mit Flask, Datenbanken und Softwarestrukturen in Python praktisch zu erlernen.
#Dadurch konnten Erfahrungen in den Bereichen Webentwicklung, Datenmodellierung, Validierung und Testen gesammelt werden.
