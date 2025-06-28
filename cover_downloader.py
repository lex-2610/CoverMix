import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment variables
token = os.getenv('SPOTIFY_TOKEN')

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

def read_albums_from_file(filename):
    albums = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if line.strip().startswith('- '):
                    album_name = line.strip()[2:]  # Remove '- ' prefix
                    albums.append(album_name)
    except FileNotFoundError:
        print(f"Datei {filename} nicht gefunden!")
    return albums

def search_album_cover(album_with_artist):
    # Split album name and artist
    if ' - ' in album_with_artist:
        album_name, artist_name = album_with_artist.split(' - ', 1)
        query = f'album:"{album_name}" artist:"{artist_name}"'
    else:
        album_name = album_with_artist
        query = f'album:"{album_name}"'
    
    result = fetch_web_api(f'v1/search?q={query}&type=album&limit=1', 'GET')
    
    if 'albums' in result and result['albums']['items']:
        album = result['albums']['items'][0]
        if album['images']:
            # Get the highest quality image (first one is usually highest res)
            return album['images'][0]['url']
    else:
        print(f"API Error for {album_with_artist}: {result}")
    return None

def download_image(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Fehler beim Download: {e}")
        return False

def create_photos_folder():
    if not os.path.exists('photos'):
        os.makedirs('photos')

def sanitize_filename(filename):
    # Remove or replace characters that are not allowed in filenames
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def main():
    # Create photos folder if it doesn't exist
    create_photos_folder()
    
    # Read albums from musik.txt
    albums = read_albums_from_file('musik.txt')
    print(f"Gefundene Alben: {len(albums)}")
    
    successful_downloads = 0
    
    for album in albums:
        print(f"Suche Cover für: {album}")
        cover_url = search_album_cover(album)
        
        if cover_url:
            # Create safe filename
            safe_filename = sanitize_filename(album)
            filename = f"photos/{safe_filename}.jpg"
            
            if download_image(cover_url, filename):
                print(f"✓ Cover heruntergeladen: {filename}")
                successful_downloads += 1
            else:
                print(f"✗ Fehler beim Download für: {album}")
        else:
            print(f"✗ Kein Cover gefunden für: {album}")
    
    print(f"\nFertig! {successful_downloads}/{len(albums)} Cover erfolgreich heruntergeladen.")

if __name__ == "__main__":
    main()