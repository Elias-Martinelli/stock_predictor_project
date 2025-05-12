setup:
	chmod +x setup_project.sh
	./setup_project.sh

install:
	pip install -r requirements.txt

# Führt Unit-Tests mit pytest im "tests/"-Verzeichnis aus
test:
	pytest tests/

run:
	python run_pipeline.py --ticker MSFT --epochs 5

# 🔍 Code-Qualität prüfen
# Führt Flake8 aus, um Stil- und Syntaxprobleme in definierten Ordnern zu finden
lint:
	flake8 stock_predictor/ scripts/


# 🧹 Code automatisch formatieren
# Formatiert den Code nach dem Black-Styleguide in allen relevanten Ordnern
format:
	black stock_predictor/ scripts/ tests/

# 🧼 Bytecode-Dateien löschen
# Entfernt alle .pyc-Dateien im Projektverzeichnis
clean:
	find . -type f -name "*.pyc" -delete

# ⚡ FastAPI-Server starten
fastapi:
	uvicorn scripts.fastapi_server:app --reload --host 0.0.0.0 --port 8000

# 📊 Streamlit-Dashboard starten
streamlit:
	streamlit run scripts/streamlit_dashboard.py

# 🐳 Docker Deployment per Shell-Skript
docker:
	chmod +x docker_deploy.sh
	./docker_deploy.sh
