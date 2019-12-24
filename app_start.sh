npx babel frontend/src --out-dir frontend --presets react-app/prod
bin/start-nginx gunicorn -c config/gunicorn.conf.py wsgi
