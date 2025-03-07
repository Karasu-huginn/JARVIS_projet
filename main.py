import listen
import talk
import ai_connector
from utils import *
from enum import Enum
import spotify_connector
import threading


def process_answer(answer):
    try:
        print(answer["code"])
    except:
        order_code = 0
        speech = "Error when extracting order code."
        print(answer)

    request = answer["request"]
    speech = answer["talk"]
    order_code = answer["code"]

    if order_code == -2:
        # todo VERI IMPAURTENT !!
        pass

    if order_code == -1:
        # todo VERI IMPAURTENT !!
        pass

    if order_code == 0:
        talk.make_mp3(speech)
        thread = threading.Thread(target=talk.play_mp3, args=["output"])
        thread.start()

    if order_code == 42:
        orders = request
        for order in orders:
            process_answer(order)

    if order_code == 1:
        change_voice()

    if order_code == 2:
        print("lumière éteinte")

    if order_code == 3:
        print("lumière allumée")

    if order_code == 4:
        print("Lumos Maxima")

    if order_code == 5:
        print("chauffage à " + request)

    if order_code == 6:
        print("lumière extérieure on")

    if order_code == 7:
        print("lumière extérieure off")

    if order_code == 8:
        print("extinction des feux totale")

    if order_code == 101:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.create_playlist(
            request["playlist_name"],
            request["playlist_description"],
        )

    if order_code == 102:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Search for track/album/artist/playlist, "request" must be a dictionary like this {"search_type":String, "search_string":String} with the name or the lyrics of what I've asked as "search_string" but you replace spaces with "+" (Ex: "highway to hell" becomes "Highway+to+Hell) and type of what I want to search as "search_type". Will give you the type's name and id (+ artist's id and name if search_type is track or album, + playlist's description if search_type is playlist, + artist's genres if search_type is artist).
        tracks = spot_conn.search(request, "track")
        print(tracks)

    if order_code == 103:
        spot_conn = spotify_connector.SpotifyConnector()
        try:
            device_id = request["device_id"]
        except:
            spot_conn.play_music()
            return
        spot_conn.play_music_on_device(device_id)

    if order_code == 104:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.pause_music()

    if order_code == 105:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.skip_to_next()

    if order_code == 106:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.skip_to_previous()

    if order_code == 107:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.go_to_time(request["time_code"])

    if order_code == 108:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.change_volume(request["volume"])

    if order_code == 109:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.set_shuffle_state(request["state"])

    if order_code == 110:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you a certain number of the last tracks listened to as dictionary with track names and track artists names, "request" mut be a dictionary like this {"number":Int} with number being the number of last played tracks wanted. If I asked you to tell me the titles of the tracks, don't repeat what's in parenthesis of the track name unless I'm asking for the full name.

    if order_code == 111:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you a certain number of the tracks in the queue and the currently playing track as a dictionary with track names and track artists names, "request" mut be a dictionary like this {"number":Int} with number being the number tracks in queue wanted. If I asked you to tell me the titles of the tracks, don't repeat what's in parenthesis of the track nameunless I'm asking for the full name.

    if order_code == 112:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.add_to_queue(request["track_id"])

    if order_code == 113:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you a boolean indicating if the player is currently playing music or not..

    if order_code == 114:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you a list of dictionaries the device names corresponding to their device id. The name 2201117TY corresponds to my phone which is a Redmi Note 11, P0ISONW0LF-PC corresponds to my personal computer and KARASU being my laptop..

    if order_code == 115:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.change_device(request["device_id"])

    if order_code == 116:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you the name and id of the track currently playing plus the name of the artist who composed the track.

    if order_code == 117:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.repeat(request["repeat_mode"])

    if order_code == 118:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.favorite_tracks(request["track_ids"])

    if order_code == 119:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you a list of booleans of whether some musics are in my favorites or not, "request" must be a dictionary like this {"track_ids":[String,String,String]}and each String in the list track_ids must be the id of the musics to check.

    if order_code == 120:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you a dictionary of details about an album (album's type, id, name, release date, tracks(id and name for each), duration, popularity, artists(id and name for each) and number of tracks in the album), "request" must be a dictionary like this {"album_id":String} with album_id being the id of the album.

    if order_code == 121:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you a dictionary of details about an artist (artist's id, name, popularity, follower count and genres), "request" must be a dictionary like this {"artist_id":String} with artist_id being the id of the artist.

    if order_code == 122:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you a list of dictionaries containing all albums(id and name) of an artist, "request" must be a dictionary like this {"artist_id":String} with artist_id being the id of the artist.

    if order_code == 123:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you a list of dictionaries containing the 10 top most listened tracks by people of an artist with for each : track id, name and popularity, "request" must be a dictionary like this {"artist_id":String} with artist_id being the id of the artist.

    if order_code == 124:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you a list of dictionaries containing all tracks (id and name for each) of a playlist, along with playlist duration, "request" must be a dictionary like this {"playlist_id":String} with playlist_id being the id of the playlist.

    if order_code == 125:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you a dictionary of details about a playlist (playlist' description, followers count, id, name, musics number, if it is public or private and author's name), "request" must be a dictionary like this {"playlist_id":String} with playlist_id being the id of the playlist.

    if order_code == 126:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.change_playlist_name(request["playlist_id"], request["playlist_name"])

    if order_code == 127:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.change_playlist_description(
            request["playlist_id"], request["playlist_description"]
        )

    if order_code == 128:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.change_playlist_public(
            request["playlist_id"], request["playlist_public"]
        )

    if order_code == 129:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.change_playlist_collaborative(
            request["playlist_id"], request["playlist_collaborative"]
        )

    if order_code == 130:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.add_tracks_to_playlist(request["track_ids"], request["playlist_id"])

    if order_code == 131:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.remove_tracks_from_playlist(
            request["track_ids"], request["playlist_id"]
        )

    if order_code == 132:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you a list of dictionaries containing all my playlists (with for each : it's id, name, author name, author id and number of tracks in it).

    if order_code == 133:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you the url for the image of a certain playlist, "request" must be a dictionary like this {"playlist_id":String} with playlist_id being the id of the playlist you need the image from.

    if order_code == 134:
        spot_conn = spotify_connector.SpotifyConnector()
        # ? change dictionary ?
        # * To execute after having prepared an image to set to a playlist, "request" must be a dictionary like this {"playlist_id":String} with playlist_id being the id of the playlist you will change the image of.

    if order_code == 135:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you a dictionary of details of a music (track's id, name, duration, album(id, name and release date), artists(id and name) and popularity), "request" must be a dictionary like this {"track_id":String} with track_id being the id of the music you want the details of.

    if order_code == 136:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you a list of dictionaries with for each track's id, name, duration, artist name and artist id along with the total duration of all the favorites tracks' playlist.

    if order_code == 137:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.remove_fav_tracks(request["track_ids"])

    if order_code == 138:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you a dictionary of features of a track (acousticness, danceability, duration, energy, instrumentalness, key, liveness, loudness, mode, speechiness, tempo, time_signature and valence) and the description for each feature.

    if order_code == 139:
        spot_conn = spotify_connector.SpotifyConnector()
        # * (This one has a very high chance of throwing an error, use with caution) ?? THIS ONE FOR SURE ?? Gives you a dictionary with my most listened to genres for long term (1 year), medium term (6 monthes) and short term (4 weeks), genres with a higher Int value are more listened to than others.

    if order_code == 140:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.follow_playlist(request["playlist_id"])

    if order_code == 141:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.unfollow_playlist(request["playlist_id"])

    if order_code == 142:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you a list of dictionaries containing all the artists (id and name) I'm currently following.

    if order_code == 143:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.follow_artist(request["profile_type"], request["profile_ids"])

    if order_code == 144:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.unfollow_artist(request["profile_type"], request["profile_ids"])

    if order_code == 145:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you a list of booleans of whether I'm following the profiles or not, profiles can either be artists or users, "request" must be a dictionary like this {"profile_type":String,"profile_ids":[String,String]} with profile_ids being a list of all the ids of the artists or users you need info of and profile_type being either "artist" or "user" depending on which you want to know.

    if order_code == 146:
        spot_conn = spotify_connector.SpotifyConnector()
        # * Gives you a boolean of whether I'm following a playlist or not, "request" must be a dictionary like this {"playlist_id":String} with playlist_id being the id of the playlist you need the info of.


def main(listener, ai_conn):
    is_waiting = True
    is_listening = True

    while is_waiting:
        print("is waiting")
        text = listener.get_en_text()
        print(text)
        if check_for_word(text, "jarvis"):
            is_waiting = False
            thread = threading.Thread(target=talk.play_mp3, args=["listening"])
            thread.start()

    text = ""
    counter = 0
    while is_listening:
        print(text)
        added_text = listener.get_en_text()
        text += added_text
        if text == "":
            continue
        if added_text == "":
            counter += 1
        if counter == 2:
            is_listening = False

    ai_answer = ai_conn.generate_text(text)
    if ai_answer["code"] != 0:
        talk.play_mp3("order")
    process_answer(ai_answer)


if __name__ == "__main__":
    g_listener = listen.Listener()
    g_ai_connector = ai_connector.AI_Connector()
    while True:
        main(g_listener, g_ai_connector)


"""
#TODO LIST :
- AI logs

"""
