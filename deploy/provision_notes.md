# Provisioning a new site

## Required packages

- python 3
- git
- nginx
- pip
- virtualenvwrapper
- uwsgi
- mongodb
- certbot (let's encrypt)

**Server file structure and user**

Assuming user `flask` and project `pypass`

    `/home/flask/site/pypass`
    `/home/flask/virtenvs/pypass`

Add user

`useradd -m -s /bin/bash flask`

**Ubuntu, MongoDB, Python packages**

    `apt-get update`
    `apt-get install vim git nginx python-dev`
    `apt-get install python3 python3-dev python-pip`

MongoDB can be installed based on these instructions:

MongoDB can be installed based on these instructions:
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

**virtualenvwrapper set up**

    `pip install virtualenvwrapper`  

**Add to `~/.bashrc`**

    `export WORKON_HOME=$HOME/virtenvs`
    `source /usr/local/bin/virtualenvwrapper.sh`

**Make virtualenv for Python 3**

    `mkvirtualenv --python=/user/local/bin/python3.x pypass`

## Set up MongoDB


## nginx virtual host configuration

- See the `nginx/template.conf` for template.
- Set up configuration at `/etc/nginx/sites-available/pypass`

## uWSGI compilation and configuration

- Set up configuration at `/etc/uwsgi/sites/pypass.ini`
- Download uWSGI and build with no Python, so custom plugins ca be created:
    `wget http://projects.unbit.it/downloads/uwsgi-2.0.12.tar.gz`
- Unzip source to:
    `tar -xf uwsgi-<version>.tar.gz`  
    `mv uwsgi-<version> /usr/local/lib/uwsgi-<version>`
- Run this command: `make PROFILE=nolang`
- Then build plugin for Python 3.3, 3.4, etc:
    `PYTHON=python3.x ./uwsgi --build-plugin "plugins/python python3x"`
- Create directory to store plugins: `mkdir -p /usr/lib/uwsgi/plugins`
- Move recently created plugin(s) to this directory:
    `mv python3x_plugin.so /usr/lib/uwsgi/plugins/`
- Make sure to adjust permissions: `root:root 644`
- Finally, add plugin declaration to uwsgi INI file. See `uwsgi/template.ini` for template.

Alternatively, you can install LTS using `pip`:


## Upstart scripts

- Set up configuration at `/etc/init/uwsgi.conf`
- Set up configuration at `/etc/init/nginx.conf`
- See `upstart/nginx.conf` and `upstart/uwsgi.conf` for templates.

## Install and set up project, requirements

    `cd ~/sites`
    `git clone http://github.com/nicorellius/pypass.git`
    `apt-get install libjpeg8-dev postgresql-server.9.3`
    `pip install requirements.txt`

## TLS/SSL certificates

Lets Encrypt certificates can be installed using `certbot`:

    `cd /home/$USER`
    `wget https://dl.eff.org/certbot-auto`
    `chmod a+x certbot-auto`
    `./certbot-auto certonly`

Note that if you are running CloudFlare in front of your site, you need to disable DNS and HTTP proxy temporarily while you create the certificates.

## Source tree

- See `source_tree.md` for more information.

