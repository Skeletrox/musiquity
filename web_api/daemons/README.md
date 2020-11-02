## Daemons

Daemons must always have an exportable callable object that will allow for seamless multithreaded (or async) execution with the web API. All callables will be imported in `daemons.py` which will then export those to `manage.py` under `web_api`.