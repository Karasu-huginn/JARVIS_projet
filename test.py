from utils import *
import talk
from datetime import datetime
import json
import spotify_connector
import ai_connector
from main import process_answer
import threading
import os
import base64
from dataclasses import dataclass


"""To test :
- search for album
- search for artist
- search for playlist
- play track (with device indication)
- pause track
- skip track
- previous track
- go to time track
- volume
- shuffle
- last played tracks
- get queue
- add track to queue
- get_player_state
- get_devices
- change_device
- get_current_track
- repeat
- add tracks to favorites
- get album infos
- get artist infos
- get artist albums
- get artist top tracks
- get playlist infos
- get playlist tracks
- change playlist name
- change playlist desc
- change playlist public
- change playlist collab
- add tracks to playlist
- remove tracks from playlist
- get my playlists
- get playlist image url
- change playlist image
- get track full infos
- get fav tracks
- remove fav track
- get recent top genres
- follow playlist
- unfollow playlist
- follow artist
- unfollow artist
- is_artist_followed
- is_playlist_followed
- get followed artists
"""
