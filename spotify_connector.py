import requests
import json
from datetime import datetime
import utils
from utils import SizeError
import os
import base64
from deprecated import deprecated

REDIRECT_URI = "https://erwannquin.fr"
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"


class SpotifyConnector():
    def __init__(self):
        file = open(f"spotify_token.json","r").read()
        spot_infos = json.loads(file)
        self.client_id = spot_infos["client_id"]
        self.client_secret = spot_infos["client_secret"]
        self.refresh_token = spot_infos["refresh_token"]

    @deprecated
    def get_cred_token(self):
        url = "https://accounts.spotify.com/api/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        query = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
            }
        response = requests.post(url, headers=headers, data=query).json()
        self.cred_token = response["access_token"]
        #todo lancer timer expiration token (accessible avec ["expires_in"]) en utilisant l'endpoint "refresh token"

    def auth_token_save(self, token_infos):
        expires_at = datetime.now().timestamp() + token_infos['expires_in']
        token_dict = {"access_token": token_infos["access_token"], "expires_at":expires_at}
        file = open("spotify_token.json","w")
        file.write(json.dumps(token_dict))
        file.close()

    def request_auth_token(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        query = {
                'grant_type': "refresh_token",
                'refresh_token': self.refresh_token,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
        }
        response = requests.post(TOKEN_URL, headers=headers, data=query).json()
        return response

    def get_auth_token(self):
        file = open(f"spotify_token.json","r").read()
        token_infos = json.loads(file)
        token_expire = token_infos["expires_at"]
        if token_expire < datetime.now().timestamp():
            token = self.request_auth_token()
            self.auth_token_save(token)
            return token["access_token"]
        else:
            return token_infos["access_token"]
        
    def send_request(self, request_type, endpoint, params="", data=""):
        token = self.get_auth_token()
        headers = {'Authorization': 'Bearer ' + token}
        url = API_BASE_URL + endpoint
        if request_type == "post":
            response = requests.post(url, headers=headers, json=data, params=params)
        if request_type == "put":
            response = requests.put(url, headers=headers, json=data, params=params)
        if request_type == "get":
            response = requests.get(url, headers=headers, params=params)
        if request_type == "delete":
            response = requests.delete(url, headers=headers, json=data, params=params)
        return response
    
    def get_user_id(self):
        response = self.send_request("get","me").json()
        return response["id"]
    
    def create_playlist(self, playlist_name, playlist_description=""):
        spotify_user_id = self.get_user_id()
        query = {
            'name': playlist_name,
            'description': playlist_description,
            'public': False,
        }
        self.send_request("post",f"users/{spotify_user_id}/playlists", data=query)

    def search(self, search_string, search_type):
        """Possibles types : playlist, artist, track, album"""
        query = {
            'q': search_string,
            'type': search_type,
            'market': 'FR',
            'limit': '10',
        }
        response = self.send_request("get","search", params=query).json()
        items = response[f"{search_type}s"]["items"]
        elements = []

        for item in items:
            element_infos = {}
            element_infos[f"{search_type}_name"] = item["name"]
            element_infos[f"{search_type}_id"] = item["id"]
            element_artists = []

            if search_type in ["track", "album"]:
                artists = item["artists"]
                for artist in artists:
                    element_artists.append({"artist_name":artist["name"], "artist_id":artist["id"]})
                element_infos[f"{search_type}_artists"] = element_artists

            if search_type == "playlist":
                element_infos["playlist_description"] = item["description"]

            if search_type == "artist":
                element_infos["artist_genres"] = item["genres"]

            elements.append(element_infos)
        return elements
    
    def play_music(self):
        self.send_request("put","me/player/play")

    def play_music_on_device(self, device_id):
        query = {
            "device_id":device_id
        }
        self.send_request("put","me/player/play", params=query)

    def pause_music(self):
        self.send_request("put","me/player/pause")

    def skip_to_next(self):
        self.send_request("put","me/player/next")

    def skip_to_previous(self):
        self.send_request("put","me/player/previous")

    def go_to_time(self, time):
        query = {
            "position_ms":time
        }
        self.send_request("put","me/player/seek",params=query)

    def change_volume(self, volume):
        query = {
            "volume_percent":volume
        }
        self.send_request("put","me/player/volume",params=query)

    def set_shuffle_state(self, state):
        query = {
            "state":str(state).lower()
        }
        self.send_request("put","me/player/shuffle",params=query)

    def get_last_played_tracks(self, number):
        query = {
            "limit": str(number)
        }
        response = self.send_request("get","me/player/recently-played",params=query).json()
        infos = []
        for item in response["items"]:
            tracks = []
            artists = []
            tracks.append(item["track"]["name"])
            for track_artist in item["track"]["artists"]:
                artists.append(track_artist["name"])
            infos.append({"tracks":tracks,"artists":artists})
        return infos
    
    def get_queue(self):
        response = self.send_request("get","me/player/queue").json()
        queue = []
        for item in response["queue"]:
            tracks = []
            artists = []
            tracks.append(item["name"])
            for track_artist in item["artists"]:
                artists.append(track_artist["name"])
            queue.append({"tracks":tracks,"artists":artists})
        current_artists = []
        for artist in response["currently_playing"]["artists"]:
            current_artists.append(artist["name"])
        current = {"track":response["currently_playing"]["name"], "artists":current_artists}
        return {"current_track":current, "queue" : queue}
    
    def add_to_queue(self, track_id):
        query = {
            "uri": "spotify:track:"+track_id
        }
        self.send_request("post","me/player/queue",params=query)

    def get_player_state(self):
        response = self.send_request("get","me/player").json()
        return response["is_playing"]

    def get_devices(self):
        response = self.send_request("get","me/player/devices").json()
        devices = []
        for device in response["devices"]:
            infos = {"id": device["id"], "name":device["name"]}
            devices.append(infos)
        return devices

    def change_device(self, device_id):
        query = {
            "device_ids":[device_id],
            "play":True
        }
        self.send_request("put","me/player", data=query)
        
    def get_current_track(self):
        response = self.send_request("get","me/player/currently-playing").json()
        artists = []
        for artist in response["item"]["artists"]:
            artists.append(artist["name"])
        track_name = response["item"]["name"]
        track_id = response["item"]["id"]
        return {"track_id":track_id,"track_name":track_name, "track_artists":artists}

    def repeat(self, repeat_mode):
        #todo preprompt : repeat_mode on track, context or off
        query = {
            "state":repeat_mode
        }
        self.send_request("put","me/player/repeat",params=query)

    def favorite_tracks(self, track_ids):
        s_track_ids = utils.convert_list_to_str(track_ids)
        fav_tracks = self.are_tracks_favorites(s_track_ids)
        tofav_track_ids = []
        for i in range(len(track_ids)):
            if not fav_tracks[i]:
                tofav_track_ids.append(track_ids[i])
        s_tofav_track_ids = utils.convert_list_to_str(tofav_track_ids)
        query = {
            "ids": s_tofav_track_ids
        }
        self.send_request("put", "me/tracks", params=query)

    def are_tracks_favorites(self, track_ids):
        query = {
            "ids":[track_ids]
        }
        response = self.send_request("get","me/tracks/contains", params=query).json()
        return response

    def get_album_infos(self, album_id):
        response = self.send_request("get",f"albums/{album_id}").json()
        infos = {}
        infos["album_type"] = response["album_type"]
        infos["total_tracks"] = response["total_tracks"]
        infos["album_id"] = response["id"]
        infos["album_name"] = response["name"]
        infos["release_year"] = response["release_date"]
        infos["artists"] = []
        infos["tracks"] = []
        album_duration = 0
        for artist in response["artists"]:
            artist_infos = {}
            artist_infos["artist_id"] = artist["id"]
            artist_infos["artist_name"] = artist["name"]
            infos["artists"].append(artist_infos)
        for track in response["tracks"]["items"]:
            track_infos = {}
            track_infos["track_id"] = track["id"]
            track_infos["track_name"] = track["name"]
            infos["tracks"].append(track_infos)
            album_duration += track["duration_ms"]
        infos["album_popularity"] = response["popularity"]
        infos["album_duration"] = utils.convert_time(album_duration)
        return infos

    def get_artist_infos(self, artist_id):
        response = self.send_request("get",f"artists/{artist_id}").json()
        infos = {}
        infos["followers"] = response["followers"]["total"]
        infos["genres"] = response["genres"]
        infos["artist_id"] = response["id"]
        infos["artist_name"] = response["name"]
        infos["artist_popularity"] = response["popularity"]
        return infos

    def get_artist_albums(self, artist_id):
        query = {
            "include_groups":"album"
        }
        response = self.send_request("get",f"artists/{artist_id}/albums",params=query).json()
        albums_infos = []
        for album in response["items"]:
            album_infos = {}
            album_infos["album_id"] = album["id"]
            album_infos["album_name"] = album["name"]
            albums_infos.append(album_infos)
        return albums_infos
        

    def get_artist_top_tracks(self, artist_id):
        response = self.send_request("get",f"artists/{artist_id}/top-tracks").json()
        top_tracks = []
        for track in response["tracks"]:
            track_infos = {}
            track_infos["track_id"] = track["id"]
            track_infos["track_name"] = track["name"]
            track_infos["track_popularity"] = track["popularity"]
            top_tracks.append(track_infos)
        return top_tracks
    
    def get_playlist_tracks(self, playlist_id, n, link=""):
        n+=1
        if link:
            token = self.get_auth_token()
            headers = {'Authorization': 'Bearer ' + token}
            response = requests.get(link, headers=headers).json()
        else:
            response = self.send_request("get",f"playlists/{playlist_id}/tracks").json()
        playlist_infos = {}
        tracks_infos = []
        playlist_duration = 0
        for track in response["items"]:
            track_infos = {}
            track_infos["track_id"] = track["track"]["id"]
            track_infos["track_name"] = track["track"]["name"]
            playlist_duration += track["track"]["duration_ms"]
            tracks_infos.append(track_infos)
        playlist_infos["playlist_tracks"] = tracks_infos
        playlist_infos["playlist_duration"] = playlist_duration
        if response["next"] != None:
            new_playlist_infos = self.get_playlist_tracks(playlist_id, n, response["next"])
            playlist_infos["playlist_tracks"] += new_playlist_infos["playlist_tracks"]
            playlist_infos["playlist_duration"] += new_playlist_infos["playlist_duration"]
        if n == 1:
            playlist_infos["playlist_duration"] = utils.convert_time(playlist_infos["playlist_duration"])
        return playlist_infos

    def get_playlist_infos(self, playlist_id):
        response = self.send_request("get",f"playlists/{playlist_id}").json()
        playlist_infos = {}
        playlist_infos["description"] = response["description"]
        playlist_infos["followers"] = response["followers"]["total"]
        playlist_infos["id"] = response["id"]
        playlist_infos["name"] = response["name"]
        playlist_infos["owner_name"] = response["owner"]["display_name"]
        playlist_infos["is_public"] = response["public"]
        playlist_infos["tracks_amount"] = response["tracks"]["total"]
        return playlist_infos

    def change_playlist_name(self, playlist_id, playlist_name):
        query = {
            "name":playlist_name
        }
        self.send_request("put",f"playlists/{playlist_id}", data=query)

    def change_playlist_description(self, playlist_id, playlist_description):
        query = {
            "description":playlist_description
        }
        self.send_request("put",f"playlists/{playlist_id}", data=query)

    def change_playlist_public(self, playlist_id, playlist_public):
        query = {
            "public":playlist_public
        }
        self.send_request("put",f"playlists/{playlist_id}", data=query)

    def change_playlist_collaborative(self, playlist_id, playlist_collaborative):
        query = {
            "collaborative":playlist_collaborative
        }
        self.send_request("put",f"playlists/{playlist_id}", data=query)

    def add_tracks_to_playlist(self, track_ids, playlist_id):
        new_track_ids = []
        for track_id in track_ids:
            new_track_ids.append(f"spotify:track:{track_id}")
        query = {
            "uris": utils.convert_list_to_str(new_track_ids)
        }
        self.send_request("post",f"playlists/{playlist_id}/tracks",params=query)
        
    def remove_tracks_from_playlist(self, track_ids, playlist_id):
        query = {
            "tracks":[

                ]
            }
        for track_id in track_ids:
            track = {"uri": f"spotify:track:{track_id}"}
            query["tracks"].append(track)
        self.send_request("delete",f"playlists/{playlist_id}/tracks",data=query)

    def get_my_playlists(self):
        total_playlists = 1
        offset = 0
        playlists_infos = []
        while total_playlists > 0:
            query = {
                "limit":50,
                "offset":offset
            }
            response = self.send_request("get","me/playlists",params=query).json()
            for playlist in response["items"]:
                playlist_infos = {}
                playlist_infos["playlist_id"] = playlist["id"]
                playlist_infos["playlist_name"] = playlist["name"]
                playlist_infos["playlist_owner_name"] = playlist["owner"]["display_name"]
                playlist_infos["playlist_onwer_id"] = playlist["owner"]["id"]
                playlist_infos["total_tracks"] = playlist["tracks"]["total"]
                playlists_infos.append(playlist_infos)
            total_playlists = response["total"] - offset
            offset += 50
        return playlists_infos

    def get_playlist_image(self, playlist_id):
        response = self.send_request("get",f"playlists/{playlist_id}/images").json()
        if type(response) == list:
            return response[0]["url"]
        else:
            return response["url"]

    def set_playlist_image(self, img_name, playlist_id):
        token = self.get_auth_token()
        headers = {'Authorization': 'Bearer ' + token, 'Content-type':'image/jpeg'}
        url = f"{API_BASE_URL}playlists/{playlist_id}/images"
        utils.convert_to_jpeg(img_name)
        img_name = img_name.split(".")[0]
        if os.path.getsize(f"img/{img_name}.jpeg") > 256000:
            raise SizeError(f"{img_name}.jpeg is too big")
        with open(f"img/{img_name}.jpeg", "rb") as img:
            encoded_img = base64.b64encode(img.read())
        requests.put(url, headers=headers, data=encoded_img)


    def get_track_full_infos(self, track_id):
        response = self.send_request("get",f"tracks/{track_id}").json()
        track_infos = {}
        album_infos = {}
        album_infos["album_id"] = response["album"]["id"]
        album_infos["album_name"] = response["album"]["name"]
        album_infos["album_release_year"] = response["album"]["release_date"]
        track_infos["album"] = album_infos
        artists_infos = []
        for artist in response["artists"]:
            artist_infos = {}
            artist_infos["artist_id"] = artist["id"]
            artist_infos["artist_name"] = artist["name"]
            artists_infos.append(artist_infos)
        track_infos["artists"] = artists_infos
        track_infos["track_id"] = response["id"]
        track_infos["track_name"] = response["name"]
        track_infos["track_duration"] = utils.convert_time(response["duration_ms"])
        track_infos["track_popularity"] = response["popularity"]
        return track_infos

    def get_fav_tracks(self):
        total_tracks = 1
        offset = 0
        tracks_infos = []
        favs_duration = 0
        while total_tracks > 0:
            query = {
                "limit":50,
                "offset":offset
            }
            response = self.send_request("get","me/tracks", params=query).json()
            for track in response["items"]:
                track_infos = {}
                track_infos["track_id"] = track["track"]["id"]
                track_infos["track_name"] = track["track"]["name"]
                artists_infos = []
                for artist in track["track"]["artists"]:
                    artist_infos = {}
                    artist_infos["artist_id"] = artist["id"]
                    artist_infos["artist_name"] = artist["name"]
                    artists_infos.append(artist_infos)
                track_infos["artists"] = artists_infos
                favs_duration += track["track"]["duration_ms"]
                tracks_infos.append(track_infos)
            total_tracks = response["total"] - offset
            offset += 50
        favs_duration = utils.convert_time(favs_duration)
        return {"fav_tracks":tracks_infos, "total_fav_playlist_duration":favs_duration}

    def remove_fav_tracks(self, track_ids):
        query = {
            "ids":utils.convert_list_to_str(track_ids)
        }
        self.send_request("delete","me/tracks",params=query)

    def get_track_audio_features(self, track_id):
        response = self.send_request("get",f"audio-features/{track_id}").json()
        track_infos = {}
        track_infos["acousticness"] = response["acousticness"]
        track_infos["danceability"] = response["danceability"]
        track_infos["duration_ms"] = response["duration_ms"]
        track_infos["energy"] = response["energy"]
        track_infos["instrumentalness"] = response["instrumentalness"]
        track_infos["key"] = response["key"]
        track_infos["liveness"] = response["liveness"]
        track_infos["loudness"] = response["loudness"]
        track_infos["mode"] = response["mode"]
        track_infos["speechiness"] = response["speechiness"]
        track_infos["tempo"] = response["tempo"]
        track_infos["time_signature"] = response["time_signature"]
        track_infos["valence"] = response["valence"]
        track_infos["acousticness_description"] = "A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic."
        track_infos["danceability_description"] = "Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable."
        track_infos["duration_ms_description"] = "The duration of the track in milliseconds."
        track_infos["energy_description"] = "Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy."
        track_infos["instrumentalness_description"] = 'Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.'
        track_infos["key_description"] = "The key the track is in. Integers map to pitches using standard Pitch Class notation. E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1."
        track_infos["liveness_description"] = "Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live."
        track_infos["loudness_description"] = "The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db."
        track_infos["mode_description"] = "Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0."
        track_infos["speechiness_description"] = "Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks."
        track_infos["tempo_description"] = "The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration."
        track_infos["time_signature_description"] = 'An estimated time signature. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure). The time signature ranges from 3 to 7 indicating time signatures of "3/4", to "7/4".'
        track_infos["valence_description"] = "A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry)."
        return track_infos

    def get_top_genres(self, term):
        """term can be : long/medium/short for 1year/6monthes/4weeks"""
        query = {
            "time_range":f"{term}_term",
            "limit":50
        }
        response = self.send_request("get",f"me/top/artists",params=query).json()
        listened_genres = {}
        for artist in response["items"]:
            genres = artist["genres"]
            for genre in genres:
                if genre in listened_genres:
                    listened_genres[genre] += 1
                else:
                    listened_genres[genre] = 1
        return listened_genres

    def follow_playlist(self, playlist_id):
        query = {
            "public":False
        }
        self.send_request("put", f"playlists/{playlist_id}/followers", data=query)

    def unfollow_playlist(self, playlist_id):
        self.send_request("delete", f"playlists/{playlist_id}/followers")

    def get_followed_artists(self):
        artists_infos = []
        is_last_page = False
        last_artist = ""
        while not is_last_page:
            query = {
                "type":"artist",
                "limit":50,
                "after":last_artist
            }
            response = self.send_request("get", "me/following", params=query).json()
            for artist in response["artists"]["items"]:
                artist_infos = {}
                artist_infos["name"] = artist["name"]
                artist_infos["id"] = artist["id"]
                artists_infos.append(artist_infos)
            if response["artists"]["cursors"]["after"] == None:
                is_last_page = True
            else:
                last_artist = response["artists"]["cursors"]["after"]
        return artists_infos

    def follow_artist(self, profile_type, profile_ids):
        """profile_type can be artist/user"""
        query = {
            "type":profile_type,
            "ids":utils.convert_list_to_str(profile_ids)
        }
        self.send_request("put", "me/following", json=query)

    def unfollow_artist(self, profile_type, profile_ids):
        """profile_type can be artist/user"""
        query = {
            "type":profile_type,
            "ids":utils.convert_list_to_str(profile_ids)
        }
        self.send_request("delete", "me/following", json=query)

    def is_artist_followed(self, profile_type, profile_ids):
        """profile_type can be artist/user"""
        query = {
            "type":profile_type,
            "ids":utils.convert_list_to_str(profile_ids)
        }
        response = self.send_request("get", "me/following/contains", params=query).json()
        return response

    def is_playlist_followed(self, playlist_id):
        response = self.send_request("get",f"playlists/{playlist_id}/followers/contains").json()
        return response



if __name__ == "__main__":
    conn = SpotifyConnector()
    
    #* connector test space
