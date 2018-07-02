# ucsd-bisb-unofficial
The unofficial information hub for students in the Bioinformatics and Systems Biology graduate program at UCSD. If you have any questions about it, contact Tony (aaylward@eng.ucsd.edu).

## How to contribute
First, if you haven't yet, spend a few hours getting familiar with [HTML](https://developer.mozilla.org/en-US/docs/Learn/HTML), [CSS](https://developer.mozilla.org/en-US/docs/Learn/CSS), and [Flask](http://flask.pocoo.org). (Optionally, you might also want to look at [Bootstrap](https://getbootstrap.com/docs/4.1/getting-started/introduction/).) It might seem like a lot, but don't worry - all you need is a very basic understanding of how each of these things works. Most of the heavy lifting is taken care of by frameworks, so there's no need to read about all the details. It's better to just start developing!

The best place to start might be the official [Flask tutorial](http://flask.pocoo.org/docs/1.0/tutorial/). [This other Flask tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) is a bit dated but the first few chapters are also worth a look (as an introduction to [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/).) [Yet another Flask Tutorial](http://www.patricksoftwareblog.com/flask-tutorial/) is also available.

Once you're ready, create your own fork of this repository, clone the fork to your local machine and navigate to the working directory. When inside, do the following:
```
python3 -m venv venv
source venv/bin/activate
pip3 install -e .
pip3 install pytest
export FLASK_APP=ucsd_bisb_unofficial
export FLASK_ENV=development
flask db upgrade
pytest
flask run
```
Congratulations! You're now running the Flask development server, and you can view your local version of the site by navigating to [http://localhost:5000](http://localhost:5000) in a web browser. Changes you make to the HTML or Python code will be reflected in the browser window. Changes to the CSS should also be reflected, but you may need to clear your browser's cache to see them.

Once you're ready to suggest your changes to the main site, use [pytest](https://docs.pytest.org/en/latest/) to make sure all the unit tests pass. Then push up to your forked repository and send a pull request. Thanks for your help!

## On the production server
```
python3 setup.py bdist_wheel
source venv/bin/activate
pip3 install -r requirements.txt dist/ucsd_bisb_unofficial-[latest]-py3-none-any.whl
python3 production_config/__init__.py venv/var/ucsd_bisb_unofficial-instance/
cd venv/var/ucsd_bisb_unofficial-instance/
export FLASK_APP=ucsd_bisb_unofficial
flask db upgrade
```
See also a [neat video on uWSGI](https://www.youtube.com/watch?v=2IeSPvkQEtw)
