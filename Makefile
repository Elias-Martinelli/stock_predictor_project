# 🐳 Docker Deployment per Shell-Skript
setup:
	chmod +x setup_project.sh
	./setup_project.sh

install:
	pip install -r requirements.txt

test:
	pytest tests/

run:
	python run_pipeline.py --ticker MSFT --epochs 5

lint:
	flake8 stock_predictor/ scripts/

format:
	black stock_predictor/ scripts/ tests/

clean:
	find . -type f -name "*.pyc" -delete

fastapi:
	uvicorn scripts.fastapi_server:app --reload --host 0.0.0.0 --port 8000

streamlit:
	streamlit run scripts/streamlit_dashboard.py

# 🐳 Docker Deployment per Shell-Skript
docker:
	chmod +x docker_deploy.sh
	./docker_deploy.sh
