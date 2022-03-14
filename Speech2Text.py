#import threading
import speech_recognition as sr
from datetime import date
from time import sleep
from TextParser import *
from relayControl import *
from MotorControl import *

class Speech2Text:

    #motor = MotorControl()
    #r = sr.Recognizer()
    #mic = sr.Microphone()
    #text = TextParser()
    #wakeWord = "pillow"

    print("hello")
    def listen(self):
        motor = MotorControl()
        r = sr.Recognizer()
        mic = sr.Microphone()
        text = TextParser()
        wakeWord = "pillow"
        
        with mic as source:
            audio = r.listen(source, phrase_time_limit=10)
                
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
            else:
                motor.relayRun(relay[1], relay[0])

        except:
            print("Failed to understand")
    def __init__(self):
        self.listen()

Speech2Text()
    
