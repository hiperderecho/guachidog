guachidog🐶
===========

Un sitio web y bot de Slack que monitorea cambios en otros sitios web.

Basado en el código de newsdiffs, escrito Eric Price (ecprice@mit.edu),
Greg Price (gnprice@gmail.com), Jennifer 8. Lee (jenny@jennifer8lee.com)

Bajo licencia MIT/Expat; ver LICENSE.
http://github.com/ecprice/newsdiffs.

guachidog funciona con las mismas instrucciones que newsdiffs, con el
requisito adicional del módulo slackclient (instalable con pip).

Para la funcionalidad de Slack es necesario crear una aplicación en Slack:
https://api.slack.com/apps

La aplicación no tiene que ser pública. Los tokens de autenticación deben
estar en settings.py (ver ejemplo).

Considerar guachidog en calidad alpha.


Instrucciones de instalación originales de newsdiffs:

Requirements
------------

You need to have installed on your local machine
* Git
* Python 2.6 or later
* Django and other Python libraries

On a Debian- or Ubuntu-based system, it may suffice (untested) to run

```
$ sudo apt-get install git-core python-django python-django-south python-simplejson
```

On Mac OS, the easiest way may be to install pip:
  http://www.pip-installer.org/en/latest/installing.html
and then

```
$ pip install Django
```

Initial setup
-------------

```
$ python website/manage.py syncdb && python website/manage.py migrate
$ mkdir articles
```

Running NewsDiffs Locally
-------------------------

Do the initial setup above.  Then to start the webserver for testing:

```
$ python website/manage.py runserver
```

and visit http://localhost:8000/

Running the scraper
-------------------

Do the initial setup above.  You will also need additional Python
libraries; on a Debian- or Ubuntu-based system, it may suffice
(untested) to run

```
$ sudo apt-get install python-bs4 python-beautifulsoup
```

on a Mac, you will want something like

```
$ pip install beautifulsoup4
$ pip install beautifulsoup
$ pip install html5lib
```

Note that we need two versions of BeautifulSoup, both 3.2 and 4.0;
some websites are parsed correctly in only one version.

Then run
  
```$ python website/manage.py scraper```

This will populate the articles repository with a list of current news
articles.  This is a snapshot at a single time, so the website will
not yet have any changes. To get changes, wait some time (say, 3
hours) and run 'python website/manage.py scraper' again.  If any of
the articles have changed in the intervening time, the website should
display the associated changes.

The scraper will log progress to /tmp/newsdiffs_logging (which is
overwritten each run) and errors to /tmp/newsdiffs/logging_errs (which
is cumulative).

To run the scraper every hour, run something like:

```$ while true; do python website/manage.py scraper; sleep 60m; done```

or make a cron job.
