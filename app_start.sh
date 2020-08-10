npx babel frontend/src --out-dir frontend --presets react-app/prod
export PYTHONPATH="${PYTHONPATH}:$(pwd)/model"
bin/start-nginx gunicorn -c config/gunicorn.conf.py wsgi
