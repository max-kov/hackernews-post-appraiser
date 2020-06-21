pip install torch==1.5.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
npx babel frontend/src --out-dir frontend --presets react-app/prod
export PYTHONPATH="${PYTHONPATH}:$(pwd)/model"
bin/start-nginx gunicorn -c config/gunicorn.conf.py wsgi
