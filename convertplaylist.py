import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from urllib.parse import urlparse
from urllib.parse import parse_qs
import json
import time
from math import floor

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = "a8ff171bc7ce4489bba3203ed2c61210", client_secret = "13648f46871d4e1ea186f54c401e5b3a"))

#change url to cmd parameter
url = "https://open.spotify.com/playlist/7kbekQB77leprglhDsLm10?si=0ff1f5a94304427d"
parsed_url = urlparse(url)
userkey = parse_qs(parsed_url.query)['si'][0]
playlistkey = parsed_url.path.split("/")[2]
uri = "spotify:user:" + userkey + ":playlist:" + playlistkey


#Currently assumes first artist in the list is the only artist.
#May be an issue for songs that have no album artist defined.

def getAlbumArtist(albumkey):
    album = spotify.album(albumkey)
    artist = album["artists"][0]["name"]
    return artist

def generatePlaylistID():
    return floor(time.time() * float(1000))


playlist = spotify.playlist(playlistkey)
playlistname = playlist["name"]
playlistdesc = playlist["description"]
songs = playlist["tracks"]["items"]

mysongkeys = []
for song in songs:
    s = song["track"]
    title = s["name"]
    album = s["album"]["name"]
    albumkey = s["album"]["id"]
    albumartist = getAlbumArtist(albumkey)
    artist = s["artists"][0]["name"]
    mysongkey = title + album + albumartist + artist
    mysongkey = mysongkey.replace(",", "")
    mysongkeys.append(mysongkey)

playlistid = generatePlaylistID()

playlistdict = {
    "PlaylistID":playlistid,
    "albumname":"",
    "albumkey":None,
    "pinned":True,
    "pinnedinalbum":False,
    "isflavour":False,
    "Name":playlistname,
    "Artist":None,
    "Key":None,
    "Year":0,
    "AlbumArtSongId":None,
    "Songids":mysongkeys
}

playlistjson = json.dumps(playlistdict)
f = open(str(playlistid) + ".playlist", "w")
f.write(playlistjson)
f.close()