import cherrypy
import configparser
import logging
from multiprocessing import Queue
import requests
from urllib.parse import quote
import webbrowser

config = configparser.ConfigParser()
config.read('config.ini')
config = config['twitch.tv']
CLIENT_ID = config['CLIENT_ID']
CLIENT_SECRET = config['CLIENT_SECRET']

SCOPES = [
    'clips:edit',
]

REDIRECT_URL = 'http://localhost:8080'
API_BASE = "https://api.twitch.tv/helix"
TOKEN_URL = 'https://id.twitch.tv/oauth2/token'
AUTH_URL = f"https://id.twitch.tv/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URL}&response_type=code&scope={quote(' '.join(SCOPES))}"

class Twitch:
    def __init__(self, code):
        self.get_token(code)
        self.refresh_token = None

    def headers(self):
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Client-Id': CLIENT_ID
        }

    def clip_that(self, username):
        """Clips that shit."""
        user_id = self.get_user_id(username)
        res = requests.post(
            f'{API_BASE}/clips?broadcaster_id={user_id}',
            headers=self.headers()
        )

        logging.info(res.json())
        return res.json()

    def get_token(self, code):
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URL,
        }

        r = requests.post(TOKEN_URL, params=params)
        r.raise_for_status()

        data = r.json()
        self.access_token = data.get('access_token')
        self.refresh_token = data.get('refresh_token')

    def get_user_id(self, user) -> str:
        url = f'https://api.twitch.tv/helix/users?login={user}'
        r = requests.get(url, headers=self.headers())

        return r.json()['data'][0]['id']

class Swerver:
    def __init__(self, q):
        self.q = q
        self.twitch = None

    @cherrypy.expose
    def index(self, code='', scope=''):
        self.q.put(code)
        return 'You are now authorized to access the Twitch API.'

    @cherrypy.expose
    # TODO: Write edit URL to sqlite DB.
    def clip(self):
        if self.twitch is None:
            return

        me = 'DJSwerveGG'
        data = self.twitch.clip_that(me)

        if data.get('status') != requests.codes.ok:
          return
        return str(data)

if __name__ == '__main__':
    q = Queue()
    swerver = Swerver(q)
    cherrypy.tree.mount(swerver, '')
    cherrypy.engine.start()

    webbrowser.open(AUTH_URL)
    code = q.get()
    twitch = Twitch(code)
    swerver.twitch = twitch
    # TODO: Background thread that updates with refresh token every 2 minutes.
