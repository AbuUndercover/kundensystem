# start.py
# Startpunkt für die Flask-Anwendung

from app.main import app

if __name__ == "__main__":
    # Nur lokal starten, nicht auf Render
    app.run(host="0.0.0.0", port=5000, debug=True)