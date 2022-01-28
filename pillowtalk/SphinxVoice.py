import speech_recognition as voice
class sphinxVoice:

	def __init__(self):
		self.r = voice.Recognizer()
		self.m = voice.Microphone()
		with self.m as source:
			self.r.adjust_for_ambient_noise(source)

	def listenControl(self):
		print ("hello")
		with self.m as source:
			audio = self.r.listen(source)
			try:
    				print("Sphinx thinks you said: " + self.r.recognize_sphinx(audio))
			except voice.UnknownValueError:
				print("Sphinx could not understand audio")
			except voice.RequestError as e:
				print("Sphinx error; {0}".format(e))

	def readjustAmbientNoise(self):
		self.r.adjust_for_ambient_noise(source)
