Uncertain Dashboard
===================
Uncertain Dashboard is a simple, and potentially unsafe, dashboard made with Python and Flask for viewing systemd services and disks. Use at your own risk! The dashboard requires root access so it can use the smartctl command and start/stop and restart services. There is also no authentication so if you use this you need to handle that somehow, webserver authentication for example. 

![Uncertain Dashboard screenshot](http://i.imgur.com/9XmhwGA.png "Uncertain Dashboard screenshot")

# Installing
------------
## Installation Requirements
 - `python` >= 3.3
 - `python3-dev`
 - `python-dbus` for python 3
 - `smartmontools`
 - `git`

## Commands
```
git clone https://github.com/temeez/uncertain-dashboard
cd uncertain-dashboard
virtualenv --system-site-packages --python=python3 venv
python setup.py install
```
Then setup nginx and [uWSGI](http://flask.pocoo.org/docs/0.10/deploying/uwsgi/) or what ever you prefer.

# uWSGI and Nginx
------------
## uncertain-dashboard.ini
```
[uwsgi]
base = /www/%n

master = true
module = uncertaind
callable = app
uid = root
gid = nginx
home = %(base)/venv
pythonpath = %(base)
plugin = /root/uwsgi/python34_plugin.so
processes = 4
socket = /var/run/%n.sock
chown-socket = nginx:nginx
chmod-socket = 660
vacuum = true
pidfile = /var/run/%n.uwsgi.pid
logto = /var/log/uwsgi/%n.log
import = task
manage-script-name = true
mount = /%n=%(module):%(callable)
```

# uncertain-dashboard.conf
```
server {
    listen 80;
    server_name dash.local;

    access_log /var/log/nginx/${host}.access.log;
    error_log /var/log/nginx/${host}.error.log;

    location = favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /www/uncertain-dashboard/uncertaind;
    }

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/var/run/uncertain-dashboard.sock;
    }
}
```

# Problems
------------
**ImportError: No module named dbus**
: Install `python-dbus` for python 3 and make sure that the virtualenv can use the python-dbus system package `--system-site-packages`
