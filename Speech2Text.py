import speech_recognition as sr
from datetime import date
from time import sleep

r = sr.Recognizer()
mic = sr.Microphone()

print("hello")

while True:
    with mic as source:
        audio = r.listen(source)
        
    try:
        words = r.recognize_google(audio)
        print(words)
        if words == "exit":
            print("...")
            sleep(1)
            print("...")
            sleep(1)
            print("...")
            sleep(1)
            print("Goodbye")
            break
    except:
        print("Failed to understand")
