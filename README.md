# ucsd-bisb.info

On the server:
```
python3 setup.py bdist_wheel
python3 -m venv venv
source venv/bin/activate
pip3 install dist/flaskr-1.0.0-py3-none-any.whl
cd venv/lib
export FLASK_APP=flaskr
flask init-db
```
