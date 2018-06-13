# ucsd-bisb-unofficial

Locally for development:
```
python3 -m venv venv
source venv/bin/activate
pip3 install -e .
pip3 install pytest coverage
pytest
coverage run -m pytest
coverage report
```

On the server:
```
python3 setup.py bdist_wheel
python3 -m venv venv
source venv/bin/activate
pip3 install dist/ucsd_bisb_unofficial-0.0.1-py3-none-any.whl
cd venv/lib/python3.6/site-packages/
export FLASK_APP=ucsd_bisb_unofficial
flask init-db
python3 configure_secret_key/__init__.py ../../../var/ucsd_bisb_unofficial-instance/
```
