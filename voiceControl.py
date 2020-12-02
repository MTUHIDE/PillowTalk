import speech_recognition as voice

r = voice.Recognizer()
with voice.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# recognize speech using Sphinx
try:
    print("Sphinx thinks you said: " + r.recognize_sphinx(audio))
except voice.UnknownValueError:
    print("Sphinx could not understand audio")
except voice.RequestError as e:
    print("Sphinx error; {0}".format(e))
