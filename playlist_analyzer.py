import requests
import json

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment variables
token = os.getenv('SPOTIFY_TOKEN')
playlist_name = os.getenv('PLAYLIST_NAME', 'Lieblingssongs')

if not token:
    print("❌ SPOTIFY_TOKEN nicht in .env gefunden!")
    print("Bitte konfiguriere deine .env Datei mit:")
    print("SPOTIFY_TOKEN=dein_token_hier")
    exit(1)

def fetch_web_api(endpoint, method, body=None):
    url = f"https://api.spotify.com/{endpoint}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        headers['Content-Type'] = 'application/json'
        response = requests.post(url, headers=headers, data=json.dumps(body) if body else None)
    
    return response.json()

def get_playlist_tracks(playlist_name):
    # Get user's playlists
    playlists = fetch_web_api('v1/me/playlists', 'GET')
    
    # Find the "Lieblingssongs" playlist
    target_playlist = None
    for playlist in playlists['items']:
        if playlist['name'].lower() == playlist_name.lower():
            target_playlist = playlist
            break
    
    if not target_playlist:
        print(f"Playlist '{playlist_name}' nicht gefunden!")
        return []
    
    # Get tracks from the playlist
    playlist_id = target_playlist['id']
    result = fetch_web_api(f'v1/playlists/{playlist_id}/tracks', 'GET')
    return [item['track'] for item in result.get('items', []) if item['track']]

playlist_tracks = get_playlist_tracks(playlist_name)
albums = set()

for track in playlist_tracks:
    album_name = track['album']['name']
    artist_name = track['album']['artists'][0]['name']  # First artist
    album_with_artist = f"{album_name} - {artist_name}"
    albums.add(album_with_artist)

with open('musik.txt', 'w', encoding='utf-8') as f:
    f.write(f"Alben aus der Playlist '{playlist_name}':\n")
    for album in sorted(albums):
        f.write(f"- {album}\n")

print("Alben wurden in musik.txt gespeichert!")