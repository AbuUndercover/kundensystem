# setup_db.py
# Dieses Skript richtet die Datenbank ein und führt die Migration für neue Spalten aus.
# Warum: So stellen wir sicher, dass die DB immer den aktuellen Stand hat.

from db import datenbank_initialisieren, migration_schritt_1, kurztest_spalten

if __name__ == "__main__":
    # Tabellen anlegen (falls es die DB noch nicht gibt)
    datenbank_initialisieren()

    # Migration Schritt 1: PLZ (kunden) + STATUS (auftraege) ergänzen, falls sie fehlen
    migration_schritt_1()

    # Kleiner Test: Spaltenliste ausgeben
    spalten = kurztest_spalten()
    print("✅ Datenbank fertig. Spaltenübersicht:")
    print(" - kunden:", ", ".join(spalten["kunden"]))
    print(" - auftraege:", ", ".join(spalten["auftraege"]))
