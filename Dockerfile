# Dockerfile – Streamlit Dashboard für dein Projekt
FROM python:3.10-slim

WORKDIR /app

# Systemabhängigkeiten für Visualisierung (z. B. matplotlib, TensorFlow)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Python-Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Projektcode kopieren
COPY . .
RUN pip install -e .

# Streamlit-Port freigeben
EXPOSE 8501

# Streamlit App starten
CMD ["streamlit", "run", "scripts/streamlit_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
