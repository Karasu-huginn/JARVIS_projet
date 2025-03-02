import listen
import talk
import ai_connector
from utils import *
from enum import Enum
import spotify_connector
import threading


def process_answer(answer):
    #todo code for AI question + todo in preprompt
    try:
        print(answer["code"])
    except:
        print(answer)

    order_code = answer["code"]

    if order_code == -2:
        #todo VERI IMPAURTENT !!
        pass

    if order_code == -1:
        #todo VERI IMPAURTENT !!
        pass

    if order_code == 0:
        talk.make_mp3(answer["request"])
        thread = threading.Thread(target=talk.play_mp3, args=["output"])
        thread.start()

    if order_code == 42:
        #todo refactor: changing to classic list
        orders = answer["request"].split(";")
        for order in orders:
            process_answer({"code":order})
    
    if order_code == 1:
        change_voice()

    if order_code == 2:
        print("lumière éteinte")

    if order_code == 3:
        print("lumière allumée")

    if order_code == 4:
        print("Lumos Maxima")

    if order_code == 5:
        print("chauffage à " + answer["request"])

    if order_code == 6:
        print("lumière extérieure on")

    if order_code == 7:
        print("lumière extérieure off")

    if order_code == 8:
        print("extinction des feux totale")

    if order_code == 101:
        spot_conn = spotify_connector.SpotifyConnector()
        spot_conn.create_playlist(answer["request"]["playlist_name"], answer["request"]["playlist_description"])
        print(f"playlist {answer["request"]["playlist_name"]} created")

    if order_code == 102:
        spot_conn = spotify_connector.SpotifyConnector()
        tracks = spot_conn.search(answer["request"], "track")
        print(tracks)

    if order_code == 103:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 104:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 105:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 106:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 107:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 108:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 109:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 110:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 111:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 112:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 113:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 114:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 115:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 116:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 117:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 118:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 119:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 120:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 121:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 122:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 123:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 124:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 125:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 126:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 127:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 128:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 129:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 130:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 131:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 132:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 133:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 134:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 135:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 136:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 137:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 138:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 139:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 140:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 141:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 142:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 143:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 144:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 145:
        spot_conn = spotify_connector.SpotifyConnector()

    if order_code == 146:
        spot_conn = spotify_connector.SpotifyConnector()

def main(listener, ai_conn):
    is_waiting = True
    is_listening = True

    while is_waiting:
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
            counter+=1
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