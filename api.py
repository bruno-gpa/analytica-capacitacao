import spotipy.util as util
import spotipy
import requests


class SpotifyAPI:
	def __init__(self):
		self.url = 'https://api.spotify.com/v1/'
		self.access = self.get_client_info()

	def get_client_info(self):
		access = []
		with open('access.txt', 'r') as f:
			for line in f:
				line = line.rstrip('\n')
				access.append(line)
		return access

	def get_token(self):
		self.token = util.prompt_for_user_token(username=self.access[0], client_id=self.access[1], 
												client_secret=self.access[2], redirect_uri=self.access[3], 
												scope=self.access[4])
		self.headers = {
			'Accept': 'application/json',
			'Content-Type': 'application/json',
			'Authorization': f'Bearer ' + self.token,}

	def get_id(self, track_name):
		self.get_token()
		params = [('q', track_name), ('type', 'track')]

		try:
			response = requests.get(f'{self.url}search', headers=self.headers, params=params, timeout=5)
			json = response.json()
			result = json['tracks']['items'][0]
			track_id = result['id']
			return track_id
		except Exception as e:
			print(e)
			return None

	def get_features(self, track_id):
		self.get_token()
		spotify = spotipy.Spotify(auth=self.token)

		try:
			features = spotify.audio_features([track_id])
			return features
		except Exception as e:
			print(e)
			return None
