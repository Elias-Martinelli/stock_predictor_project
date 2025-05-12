# 📈 Stock Predicto
Ein umfassendes, LSTM-basiertes Machine-Learning-Projekt zur Vorhersage von Aktienkursen. Die Anwendung kombiniert eine leistungsfähige REST-API mit einem interaktiven Streamlit-Dashboard und einem vollständig containerisierten Setup über Docker. Ziel ist es, historische Aktienkurse zu analysieren und zukunftsgerichtete Prognosen für verschiedene Unternehmen bereitzustellen.

---

## 📂 Projektstruktur

```bash
📦 STOCK_PREDICTOR_PROJECT
├── models/                      # Gespeicherte Modelle (.keras, .h5, etc.)
│   └── lstm_msft.keras
│
├── notebooks/                  # Explorative Jupyter Notebooks
│   ├── exploration.ipynb
│   └── setup.ipynb
│
├── scripts/                    # Startskripte für Server, Dashboard, etc.
│   ├── fastapi_server.py       # FastAPI REST-API
│   └── streamlit_dashboard.py  # Streamlit-Frontend
│
├── stock_predictor/            # Hauptmodul mit Kernfunktionen
│   ├── __init__.py
│   ├── data_loader.py
│   ├── model_building.py
│   └── training_pipeline.py
│
├── tests/                      # Unit Tests
│   ├── test_data_loader.py
│   └── test_model_building.py
│
├── .env                        # Umgebungsvariablen (nicht tracken!)
├── .gitignore                  # Dateien/Ordner, die Git ignorieren soll
├── .python-version             # Python-Version für pyenv
│
├── autotest.sh                 # Automatisierungsskript für Tests, Linting, etc.
├── docker_deploy.sh            # Optionales Deployment-Skript
├── docker-compose.yml          # Mehrere Docker-Container definieren
├── Dockerfile                  # Container für das Projekt
├── Dockerfile.api              # Separater Container für API-Server (optional)
│
├── Makefile                    # Automatisierung über make
├── README.md                   # Hauptdokumentation des Projekts
├── requirements.txt            # Python-Abhängigkeiten
├── setup.py                    # Setup-Skript für Package-Installation
├── setup_project.sh            # Setup-Automatisierung (z. B. venv, deps)

```


---

## ⚙️ Setup & Installation

### 1. Lokale Umgebung mit pyenv + direnv

```bash
pyenv install 3.10.6
pyenv virtualenv 3.10.6 stock_predictor_env
pyenv activate stock_predictor_env
```

### 2. Projekt einrichten

```bash
chmod +x setup_project.sh
./setup_project.sh
```

> Voraussetzungen: `pyenv`, `pyenv-virtualenv`, `direnv` (empfohlen zur automatischen Aktivierung der Umgebung)

### 3. Manuelle Abhängigkeiten (optional)

```bash
pip install -r requirements.txt
```

> Tipp: Verwende `pip freeze > requirements.txt` zur Aktualisierung der Abhängigkeiten.

---

## 🚀 Schnellstart

### Starte REST API (FastAPI-Server):

```bash
make fastapi
```

Zugriff: [http://localhost:8000](http://localhost:8000)

### Starte Dashboard (Streamlit-Oberfläche):

```bash
make streamlit
```

Zugriff: [http://localhost:8501](http://localhost:8501)

> Alternativ kannst du die Docker-Variante nutzen: `make docker`

---

## 🛋️ REST API Dokumentation (FastAPI)

### Base URL:

`http://localhost:8000/docs`

### Verfügbare Endpoints:

| Methode | Pfad       | Beschreibung                       |
| ------- | ---------- | ---------------------------------- |
| GET     | `/`        | Health Check                       |
| POST    | `/predict` | Kursprognose für die nächsten Tage |

### Beispiel: Vorhersage-Anfrage

```json
{
  "ticker": "AAPL",
  "days": 5
}
```

### Beispiel: API-Antwort

```json
{
  "ticker": "AAPL",
  "predictions": [172.34, 173.01, 173.58, 174.22, 174.91]
}
```

> Der API-Key wird automatisch aus der `.env` geladen.

---

## 🔎 Interaktives Dashboard (Streamlit)

### Features:

* 🔑 API-Key Auswahl & Eingabe (aus .env oder manuell)
* 📅 Auswahl von Tickersymbolen (AAPL, MSFT, IBM etc.)
* 📊 Visualisierung von geladenen Kursdaten
* 🔄 Skalierung & Sequenzbildung für LSTM-Training
* 🚀 Live-Modelltraining mit Keras-Ausgabe
* 📈 Visualisierung von Vorhersage vs. Realwerten
* 🗃️ Modell speichern als `.keras`

### Start:

```bash
streamlit run scripts/streamlit_dashboard.py
```

> Hinweis: Für Visualisierung wird `matplotlib` verwendet (bereits installiert).

---

## 🚧 Docker & Deployment

### Lokales Multi-Service Deployment:

```bash
make docker
```

### Container-Dienste:

| Dienst    | Port | Beschreibung             |
| --------- | ---- | ------------------------ |
| stock-api | 8000 | REST API mit FastAPI     |
| dashboard | 8501 | Streamlit Web-Oberfläche |

### Docker Einzelstart (optional):

```bash
docker build -f Dockerfile.api -t stock-api .
docker run -p 8000:8000 stock-api
```

> Nutze `docker-compose logs` oder `docker ps`, um Status und Logs zu prüfen.

---

## 🛠️ Automatisierung via Makefile

```bash
make install       # Python-Abhängigkeiten installieren
make test          # Tests mit pytest starten
make lint          # Code-Qualität prüfen (flake8)
make format        # Code formatieren mit black
make docker        # Docker Deployment starten
make autotest      # Ausführen von autotest.sh (CI-Test)
```

---

## 📅 Tests & Qualitätssicherung

### Manuelle Ausführung:

```bash
pytest tests/
```

oder per

```bash
make test
```

### Abgedeckte Komponenten:

* `fetch_alpha_vantage`: Datenbeschaffung von Alpha Vantage API
* `build_and_train_model`: Modellarchitektur und Trainingslogik
* `predict_and_inverse`: Vorhersage + Invers-Transformation

### CI-Vorbereitung via `autotest.sh`

* Linting mit `flake8`
* Formatierung mit `black`
* Testlauf mit `pytest`
* Exit-Codes für CI-kompatibles Verhalten

---

## 📓 Jupyter Notebooks

Im Ordner `notebooks/` befinden sich zwei zentrale Dateien:

* **`setup.ipynb`**
  Dient zum schnellen Laden und Testen der wichtigsten Imports und Bibliotheken.

* **`exploration.ipynb`**
  Zum experimentell mit Daten arbeiten, Modelle analysieren oder spezifische Vorverarbeitungsschritte testen. Ideal für schnelles Prototyping ausserhalb der API- oder Streamlit-Pipeline.

> 💡 Notebooks helfen besonders beim Debuggen, Visualisieren von Daten und Validieren einzelner Funktionsblöcke.

---
## 💼 Projektbeschreibung

**"Stock Predictor"** ist ein vollständiges Machine-Learning-Projekt zur Prognose von Aktienkursen. Es basiert auf historischen Kursdaten, verarbeitet diese in einer LSTM-Sequenzstruktur, und bietet interaktive sowie API-basierte Schnittstellen zur Nutzung der Vorhersagemodelle.

### Technologiestack:

* Programmiersprache: **Python 3.10**
* ML: **TensorFlow**, **Keras**, **scikit-learn**
* API: **FastAPI**
* GUI: **Streamlit**
* Containerisierung: **Docker**, **Docker Compose**
* Automatisierung: **Makefile**, **autotest.sh**, **pyenv**, **direnv**

### Besonderheiten:

* `.env`-basierte Konfiguration für sichere API-Key-Verwaltung
* Reproduzierbarer Environment-Aufbau via `setup_project.sh`
* Modularisierte Python-Pakete mit `setup.py`
* Separater FastAPI- und Streamlit-Dienst
* Getrennte Dockerfiles für Frontend/Backend
* Entwicklungsfreundlich durch `make`, `pytest` und `black`

---

## 👥 Credits & Dank

* **Autor**: Elias Martinelli
* **Projektkontext**: Kursarbeit für das Modul *\[Modulname einsetzen]* bei *\[Dozent/in eintragen]*
* **Datenquelle**: [Alpha Vantage](https://www.alphavantage.co/) (kostenlose Finanzdaten-API)

> Besonderer Dank an die Lehrveranstaltung und Kommiliton\:innen für das Peer Review und Feedback!
