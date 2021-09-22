class TextParser:
    def saveCommand(self, command):
	counter = 0
	f = None
	try:
	    f = open("commandDB", 'r')
	except IOError:
	    print("file cannot be read")
	else:
            for line in f:
                pass
            if line != None:
		word = line.split(':')[0]
                if word.isdigit():
                    counter = int(word)
	    f.close()
	try:
	    f = open("commandDB", 'a')
	except IOError:
	    print("cannot open commandDB. Major Issue")
	else:
	    counter = counter + 1
	    f.write(str(counter)+ ": " + command + "\n")
	    f.close()
