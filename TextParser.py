import datetime
class TextParser:
    def saveString(self, string):
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
	    f.write("{0}: '{1}' {2}\n".format(counter, command, datetime.datetime.now()))
	    f.close()

    def commandSearch(self, string, keyword = None,):
	#self.saveString(string)
	words = string.split()
	command = None
	if keyword != None:
	    try:
	    	index = words.index(keyword)
	    	command = words[index:index+4]
	    	print("Command: {0}".format(command))
	    	print("found keyword '{0}' at index {1} in string '{2}'".format(keyword, index, string))
	    except ValueError:
		print("Index does not exist")
	else:
	    print("no keyword\n")
