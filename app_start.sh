npx babel frontend/src --out-dir frontend --presets react-app/prod
export PYTHONPATH="${PYTHONPATH}:$(pwd)/model"
gunicorn app
