import json
import sys
from vosk import Model, KaldiRecognizer
import pyaudio
import configparser


class Listener:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("settings.ini")
        en_model_path = config["PATH"]["en_speech_model_path"]
        # ? r"C:\DOSSIERS\dev\python\JARVIS_Project\vosk-model-en-us-0.42-gigaspeech")
        en_model = Model(en_model_path)
        # ? fr_model = Model(r"C:\DOSSIERS\dev\python\JARVIS_Project\vosk-model-fr-0.22")
        self.en_recognizer = KaldiRecognizer(en_model, 16000)
        # ? self.fr_recognizer = KaldiRecognizer(fr_model, 16000)
        mic = pyaudio.PyAudio()
        self.stream = mic.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8192,
        )
        self.stream.start_stream()
        print("Listener initialized.")

    def get_en_text(self):
        data = self.stream.read(4096, exception_on_overflow=False)
        if self.en_recognizer.AcceptWaveform(data):
            text = self.en_recognizer.Result()
            return text[14:-3] + " "
        else:
            return ""

    def get_fr_text(self):
        data = self.stream.read(4096)
        if self.fr_recognizer.AcceptWaveform(data):
            text = self.fr_recognizer.Result()
            return text[14:-3] + " "
        else:
            return ""
