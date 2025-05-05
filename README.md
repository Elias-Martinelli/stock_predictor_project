# 📈 Stock Predictor ML System

Willkommen zum Stock Prediction Machine Learning System!
Dieses Projekt nutzt modernste Machine Learning Techniken, um Aktienkurse vorherzusagen, Modelle live zu serven und Monitoring anzubieten.

---

## 📂 Projektstruktur

```bash
stock_predictor/
├── stock_predictor/          # Hauptpackage (Python-Module)
│   ├── __init__.py
│   ├── data_loader.py
│   ├── feature_engineering.py
│   ├── training_pipeline.py
│   ├── model_building.py
│   ├── hyperparameter_tuning_bayes.py
│   ├── backtesting.py
│   ├── metrics.py
│   ├── live_data.py
│   ├── ticker_crawler.py
├── scripts/                  # Steuerungsskripte
│   ├── run_multi_pipeline_parallel.py
│   ├── fastapi_server.py
│   ├── streamlit_dashboard.py
├── data/                      # Roh- und bearbeitete Daten
├── models/                    # Trainierte Modelle (.h5) und Scaler (.pkl)
├── tuner_results/             # Hyperparameter Tuning Ergebnisse
├── logs/                      # Fehler- und Eventlogs
├── requirements.txt           # Python-Abhängigkeiten
├── Dockerfile                 # Docker für Training & Dashboard
├── Dockerfile.api             # Docker für FastAPI Server
├── docker-compose.yml         # Alles auf einmal starten
├── README.md                  # Projektdokumentation
├── .envrc                     # direnv Setup
├── .python-version            # pyenv Setup
```


## 🚀 Setup Anleitung

Hier die genaue Reihenfolge, um das Projekt vollständig und korrekt aufzusetzen:

---

### ▶️ 1. Klonen oder Herunterladen des Projekts

```bash
git clone https://github.com/dein-repo/stock_predictor_project.git
cd stock_predictor_project
```

---

### ▶️ 2. Setup-Skript ausführbar machen

```bash
chmod +x setup_project.sh
```

---

### ▶️ 3. Setup-Skript ausführen

```bash
./setup_project.sh
```

**Was passiert hier:**
- Erstellt ein virtuelles Environment (`stock_predictor_env`) mit pyenv
- Verlinkt die Umgebung automatisch mit dem Projektordner (.python-version)
- Erstellt eine .envrc Datei für automatische Aktivierung mit direnv
- Installiert alle Packages aus requirements.txt

---


### ▶️ 4. Docker login

```bash
docker login
```
➔ Gib deinen DockerHub Username und Passwort ein.
(Hast du noch keinen Account? Kostenlos erstellen: https://hub.docker.com/)

Danach kann Docker Images von DockerHub korrekt ziehen.

---

### ▶️ 5. Docker-Deploy-Skript ausführbar machen

```bash
chmod +x docker_deploy.sh
```

---

### ▶️ 6. Docker Deployment starten

```bash
./docker_deploy.sh
```

**Was passiert hier:**
- Beendet alte Docker-Container (falls vorhanden)
- Baut neue Docker-Images (FastAPI + Streamlit)
- Startet alle Services im Hintergrund
- FastAPI verfügbar auf http://localhost:8000
- Streamlit Dashboard verfügbar auf http://localhost:8501

---

### ▶️ 7. Testen der API

Starte API Tests lokal:

```bash
python test_api_requests.py
```

**Was passiert hier:**
- Testet die `/predict-live` und `/predict` Endpoints automatisch
- Holt Live-Daten oder sendet Dummy-Daten
- Gibt JSON-Antworten der API zurück

---

## 📈 Zusammenfassung der Effekte:

| Schritt | Wirkung |
|--------|---------|
| setup_project.sh | Saubere Umgebungserstellung + Paketinstallation |
| docker_deploy.sh | Vollständiges Docker Deployment der API und Monitoring |
| API Test | Verifizierung der korrekten Funktionsweise der Prediction API |

---

## 🔥 Voraussetzungen

- Python 3.10.6
- pyenv installiert
- direnv installiert
- Docker + Docker Compose installiert

---

## ⚡ Hinweise

- `.python-version` und `.envrc` Dateien werden automatisch erstellt.
- Wenn pyenv oder direnv nicht installiert sind, muss dies manuell nachgeholt werden.
- Docker öffnet Ports 8000 (API) und 8501 (Dashboard).

---
```

---
