from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
import google_auth_oauthlib.flow
import os
import pathlib

OAUTH_REDIRECT_URI="https://localhost:8000/auth/success"
SCOPES=['https://www.googleapis.com/auth/fitness.activity.read', 'https://www.googleapis.com/auth/fitness.body.read']
CLIENT_SECRETS_FILE="{}/client_id.json".format(pathlib.Path(__file__).parent.absolute())
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

state = None
credentials = None

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


def first(request):
    global state
    # force initialization
    state = None
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES
    )

    flow.redirect_uri = OAUTH_REDIRECT_URI

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    return redirect(authorization_url)


def redirected(request):
    global state, credentials
    if not state:
        return HttpResponse("unauthorized")
    else:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
        flow.redirect_uri = OAUTH_REDIRECT_URI
        authorization_response = request.get_full_path()
        flow.fetch_token(authorization_response=authorization_response)
        my_credentials = flow.credentials
        credentials = credentials_to_dict(my_credentials)
        with open('{}/token.txt'.format(os.getcwd()), 'w') as tfile: # Write token to file. Horrible practice, man.
            tfile.write(credentials["token"])

        return HttpResponse("Authorized. Token is stored in {}/token.txt".format(os.getcwd()))

