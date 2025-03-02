import asyncio
import edge_tts
import playsound3


VOICES_FR = ['fr-FR-HenriNeural', 'fr-FR-DeniseNeural'] #todo generate french audio for french titles on spotify : ["external_ids"]["isrc"][2:] gives FR on french titles
VOICES = ['en-GB-RyanNeural', 'en-GB-SoniaNeural']
OUTPUT_FILE = "audio/output.mp3"

async def edge_tts_communicate(text)-> None:
    voice = VOICES[0]
    communicate = edge_tts.Communicate(text, voice, pitch="-5Hz")
    await communicate.save(OUTPUT_FILE)

def make_mp3(text):
        asyncio.run(edge_tts_communicate(text))

def play_mp3(file):
    playsound3.playsound(f"audio/{file}.mp3")

def talk(text):
    make_mp3(text)
    play_mp3("output")