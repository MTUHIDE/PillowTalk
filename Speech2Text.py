import speech_recognition as sr
from datetime import date
from time import sleep
from TextParser import *

r = sr.Recognizer()
mic = sr.Microphone()
text = TextParser()
wakeWord = "wake"

print("hello")

while True:
    with mic as source:
        audio = r.listen(source)
        
    try:
        words = r.recognize_google(audio)
        print(words)

        command = text.commandSearch(words, wakeWord)
        print(command)
        if command == -2:
            print("Command incomplete")
            
        relay = text.returnRelay(command)
        print(relay)
        if relay ==-1:
            print("Invalid Number")
            
        elif relay == -2:
            print("Invalid Action")
            
        elif relay == -3:
            print("Invalid Inflatable")
            
        
    except:
        print("Failed to understand")
