Uncertain Dashboard
=====================
Uncertain Dashboard is a simple dashboard made with Python and Flask for viewing systemd services and disks. 



## Installation Requirements
 - `python` >= 3.3
 - `python3-dev`
 - `python-dbus` for python 3
 - `smartmontools`
 - `git`

## Installing
```
git clone https://github.com/temeez/uncertain-dashboard
cd uncertain-dashboard
python setup.py install
```
 * Edit `config.py` and set correct postgresql infos, or use mysql/sqlite
 * Use [uWSGI](http://flask.pocoo.org/docs/0.10/deploying/uwsgi/) or such

#### Virtualenv
`virtualenv --system-site-packages --python=python3 venv`

## Problems
**ImportError: No module named dbus**
: Install `python-dbus` for python 3 and make sure that the virtualenv can use the python-dbus system package `--system-site-packages`
