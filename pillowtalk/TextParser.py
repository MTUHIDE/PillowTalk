import datetime
try:
    import MotorControl as MC
except:
    pass

class TextParser:
    def __init__(self):
        '''Initialize the text parser by pulling the dictionary.'''
        self._dictionary = self.openDictionary()
        if self._dictionary == -1:
            self._dictionary = None
            print("Dictionary was not pulled")

    def getDictValues(self, key):
        '''Obtain the values in the dictionary associated with a given key.'''
        return self._dictionary[key]

    def openDictionary(self):
        '''Attempt to open the dictionary DictionaryCommands.txt and obtain its keys and values.'''
        f = None
        keys = {}
        try:
            f = open("DictionaryCommands.txt", "r")
        except IOError:
            return -1
        else:
            tempKey = ""
            for line in f:
                # If the string contains ':', assume it is a key
                if ":" in line:
                    a = line.split(":")
                    tempKey = a[0]
                    keys[tempKey] = []  # Add the key into the dictionary
                else:
                    if line != "\n":
                        keys[tempKey].append(line.split("\n")[0])
            f.close()
            return keys

    def runCommands(self, string):
        '''Determine which motor(s) to run from the given command string.'''
        string  = string.lower().split()
        returnedMotors = self.returnMotor(string)

        if returnedMotors[1] == None:
            MC.runMotor(returnedMotors[0], returnedMotors[2])
        else:
            MC.runMotor(returnedMotors[0], returnedMotors[2])
            MC.runMotor(returnedMotors[1], returnedMotors[2])
    

    def commandSearch(self, string):
        '''Parse an input string for different command words.'''
        words = string.lower().split()
        listOfCommands = None
        keywordValues = self.getDictValues("Wakewords")
        for i, value in enumerate(keywordValues):
            try:
                index = words.index(value)
                listOfCommands = words[index + 1:]
                break
            except ValueError:
                if i == len(keywordValues) - 1:
                    raise KeywordNotFoundError("Keyword Not Found")
                continue

        if len(listOfCommands) <= 0 :
            raise InsufficientCommandLengthError("Command Not Long Enough")
        return listOfCommands

    def returnMotor(self, commands):
        '''
        Parse the commands given in the order of most recent to least recent
        to determine which motor(s) to run and for what time interval.
        Bus 1 inflates pillow 1, bus 2 deflates pillow 1, bus 3 inflates pillow 2, and bus 4 deflates pillow 2.
        '''

        # Reverse the order of commands to run from most recent to least recent.
        commands = commands[::-1]

        # Initialize the components of an instruction to null values.
        motor1 = None
        motor2 = None
        action = None
        time = None

        # Make turning off all motors the highest priority if that is found anywhere in the command string.
        values = self.getDictValues("FunctionOff")
        for value in values:
            try:
                commands.index(value)
                #MC.stopAll()
                return 0
            except ValueError:
                continue

        # Search for any mention of "inflate" or "deflate" in the command string.
        values = self.getDictValues("Functions")
        for i, value in enumerate(values):
            try:
                commands.index(value)
                action = value
                break
            except ValueError:
                if i == len(values)-1:
                    raise InvalidActionError("Action not found")
                continue
        if action == "inflate":
            motor1 = 1
            motor2 = 3
        else:
            motor1 = 2
            motor2 = 4

        leftIndex = None
        rightIndex = None
        bothIndex = None

        # Search for any mention of pillow 1 in the input string.
        values = self.getDictValues("Pillow1")
        for value in values:
            try:
                leftIndex = commands.index(value)
                break
            except:
                continue

        # Search for any mention of pillow 2 in the input string.
        values = self.getDictValues("Pillow2")
        for value in values:
            try:
                rightIndex = commands.index(value)
                break
            except:
                continue

        # Search for any mention of both pillows in the input string.
        values = self.getDictValues("PillowAll")
        for value in values:
            try:
                bothIndex = commands.index(value)
                break
            except:
                continue

        # If neither pillow was found in the input string, raise an error.
        if not bothIndex and not leftIndex and not rightIndex:
            raise InvalidActionError("Pillow assignment unknown")

        if bothIndex is None:
            bothIndex = 100000
        
        if leftIndex is None:
            leftIndex = 100000

        if rightIndex is None:
            rightIndex = 100000

        # print(f"bothIndex: {bothIndex}, leftIndex: {leftIndex}, rightIndex: {rightIndex}")

        if bothIndex < leftIndex and bothIndex < rightIndex:
            pass
        elif leftIndex < rightIndex:
            motor2 = None
        else:
            motor1 = motor2
            motor2 = None

        # Obtain the amount of time for the motor(s) to run.
        values = self.getDictValues("TimeAmount")
        for i, value in enumerate(values):
            try:
                commands.index(value)
                time = int(value)
                break
            except:
                if i == len(values)-1:
                    raise InvalidActionError("Time not found")
                continue

        # Obtain the unit of time for the motor(s) to run.
        values = self.getDictValues("TimeUnits")
        for i, value in enumerate(values):
            try:
                commands.index(value)
                if i == 1:
                    time = time * 60
                break
            except:
                if i == len(values)-1:
                    raise InvalidActionError("Unit of Time Not Found")
                continue
        print(f"Time: {time}")
        return (motor1, motor2, time)

class InsufficientCommandLengthError(Exception):
    '''Catch the lack of required arguments for a command'''

    def __init__(self, message):
        '''Print a provided message upon initialization.'''
        super().__init__(message)


class KeywordNotFoundError(Exception):
    '''Catch a keyword that does not exist'''

    def __init__(self, message):
        '''Print a provided message upon initialization.'''
        super().__init__(message)


class InvalidActionError(Exception):
    '''Catch an invalid function the pillow needs to inflate or deflate'''

    def __init__(self, message):
        '''Print a provided message upon initialization.'''
        super().__init__(message)


class NonexistentPillowError(Exception):
    '''Catch a pillow that does not exist'''

    def __init__(self, message):
        '''Print a provided message upon initialization.'''
        super().__init__(message)





def text2int(textnum, numwords={}):
    '''Convert string literal numeric values into actual numeric values.'''
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current