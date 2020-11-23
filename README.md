# Musiquity

DSCI 551 Project

## Prerequisites

Please ensure the following software is available:

* Docker and docker-compose

* npm

Please ensure the following python packages are available:

* numpy

* statsmodels

* django

* django-cors-headers

* django-sslserver

* influxdb

* django-mysql

* spotipy

## Setting up

* Create a docker volume called `influx_volume` and `mysql_volume` for persistent data storage.

* In the `musiquity_frontend` folder run `npm install`.

* Run `python recursively_dcu.py` in the root directory. This brings up the redis, Influx and MySQL dockers.

* Create a file called `config.json` in `web_api/web_api` structured as follows:

```
{
    "mysql_data": {
        "username": "mysql_username",
        "password": "mysql_password"
    }
}
```

* In `web_api/daemons`, create a file called `api.json` that is structured as follows:

```
{
    "api": {
        "key": "your_spotify_application_key",
        "secret": "your_spotify_application_secret"
    }
}
```

* In `web_api/auth_service` create a file called `client_id.json` that contains the oauth authentication details for Google authentication. (Note: Ensure that your oauth2 client can read activity and fitness data at the very least)

* Go to the `web_api` folder and run `python manage.py createsuperuser` and create a superuser for your instance.

* Then run `python manage.py runsslserver`. The SSL server is required for Google's OAuth2.

* In the `musiquity_frontend` folder, start the UI server with `npm start`.

## Initializing data

* Open `https://localhost:8080/admin/` to open the admin console and login as the superuseryou just created.

* Create a user under the 'Users' group.

* Under the Backend Service group, create the appropriate models for your cutoffs (You can poll data and use spark for this later)

* Create your "seed lists". The tracks in your seed lists must be spotify URIs for tracks separated by a comma.

* Copy your username and replace the default with it in `helpers/api_querier/api_querier.py` and `helpers/spoofers/influxdb_spoofer_delay.py`.

* Now go to `https://localhost:8080/auth` and authenticate. This should return an "authorized" message with the location of the token.txt file

## Adding data to influxDB

* When you have heart rate data recorded from a workout, run `api_querier.py <<token.txt absolute path>>` in `helpers/api_querier`. This will poll data and store it in a `points.txt` file.

* Due to issues with Google Fit Streaming, for demo purposes we shall simulate the same workout. Run `post_simulator.py`. This shall simulate data streaming.

## Getting predictions

* In `web_api/daemons` run `daemons.py`.

* If no errors come up there should be data in redis.

* Open `localhost:3000` and input your username (whatever you used in `api_querier.py`). You should see your current heart rate (with a little bit of trend) and suggestions.