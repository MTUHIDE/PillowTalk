import datetime


class TextParser:
	def saveString(self, string):
		counter = 0
		f = None
		try:
			f = open("commandDB", 'r')
		except IOError:
			pass
		else:
			for line in f:
				pass
			if line != None:
				firstWord = line.split(':', 1)[0]
				if firstWord.isdigit():
					counter = int(firstWord)
			f.close()
		try:
			f = open("commandDB", 'a')
		except IOError:
			print("cannot open commandDB. Major Issue")
		else:
			counter = counter + 1
			f.write("{0}: '{1}' {2}\n".format(counter, string, datetime.datetime.now()))
			f.close()
	#return -1 Error opening file
        def openDictionary(self):
            f = None
            try:
                f = open("commandDB", 'r')
            except IOError:
                return -1


	# return -2 command not long enough
	# return -1 keyword not found
	# return 0
	# return command
	def commandSearch(self, string, keyword=None):
		words = string.split()
		command = None
		if keyword != None:
			try:
				index = words.index(keyword)
				command = words[index + 1:index + 5]
				print("Command: {0}".format(command))
				print("found keyword '{0}' at index {1} in string '{2}'".format(keyword, index, string))
			except ValueError as e:
				# self.saveString("Keyword:'{0}' not found in '{1}'".format(keyword, string)
				print("Index does not exist")
				return -1
		else:
			command = words

		if len(command) < 3:
			return -2
		return command

	# return -1 invalid number
	# return -2 invalid action
	# return -3 invalid inflatable
	# bus 1 inflate pillow 1, bus 2 deflate pillow 1, bus 3 inflate pillow 2, bus 4 deflate pillow 2
	def returnRelay(self, command):
		relay = None
		action = command[0]
		pillow = command[1]
		time = None
		try:
			time = int(command[2])
		except ValueError as e:
			return -1

		if len(command) == 4:
			if command[3] == "minute":
				time = time * 60
		if action == "inflate":
			if pillow == "cushion_1":
				relay = 1
			elif pillow == "cushion_2":
				relay = 3
			else:
				return -3
		elif action == "deflate":
			if pillow == "cushion_1":
				relay = 2
			elif pillow == "cushion_2":
				relay = 4
			else:
				return -3
		else:
			return -2

		return [relay, time]
