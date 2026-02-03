#!/bin/bash

# Aller dans le dossier du script (IMPORTANT)
cd "$(dirname "$0")"

# Activer le venv
source venv/bin/activate

# Charger les variables d'environnement
export $(grep -v '^#' .env | xargs)

# Stopper l'ancienne instance si elle existe
pkill -f "uvicorn app.main" || true

# Lancer FastAPI en background
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > api.log 2>&1 &