#import threading
import speech_recognition as sr
from datetime import date
from time import sleep
from TextParser import *
import requests

class Speech2Text:


    print("hello")
    def listen(self):
        r = sr.Recognizer()
        mic = sr.Microphone()
        text = TextParser()
        wakeWord = "pillow"
        
        with mic as source:
            audio = r.listen(source, phrase_time_limit=10)
                
        try:
            words = r.recognize_google(audio)
            print (words)
            requests.post("http://localhost:3000/parse",json={"text": words})

        except Exception as e:
            print(e)
    def __init__(self):
        self.listen()

Speech2Text()
    
