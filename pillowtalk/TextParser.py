import datetime
from MotorControl import * as MC


class TextParser:
    def __init__(self):
        self._dictionary = self.openDictionary()
        if self._dictionary == -1:
            self._dictionary = None
            print("dictionary was not pulled")

    def getDictValues(self, key):
        return self._dictionary[key]

    def openDictionary(self):
        f = None
        keys = {}
        try:
            f = open("DictionaryCommands.txt", "r")
        except IOError:
            return -1
        else:
            tempKey = ""
            for line in f:
                # If the string contain ':' it can be assume that is is a key
                if ":" in line:
                    a = line.split(":")
                    tempKey = a[0]
                    keys[tempKey] = []  # Add the key into the dictionary
                else:
                    if line != "\n":
                        keys[tempKey].append(line.split("\n")[0])
            f.close()
            return keys

# Main function to run
    def runCommands(self, string, keyword=False):
        commandArray = self.commandSearch(string, keyword)
        if commandArray == 0:
            MC.stopAll()
            print("stopping motors")
        
        returnedMotors = returnMotor(commandArray)

    # return 0
    # return command
    def commandSearch(self, string):
        words = string.lower().split()
        listOfCommands = None
        keywordValues = self.getDictValues("Wakewords")
        for i, value in enumerate(keywordValues):
            try:
                index = words.index(value)
                listOfCommands = words[index + 1:]
                break
            except ValueError:
                if i == len(keywordValues)-1:
                    raise KeywordNotFoundError("Keyword Not Found")
                continue

        if len(listOfCommands) <= 0 :
            raise InsufficientCommandLengthError("Command Not Long Enough")
        return listOfCommands

    # bus 1 inflate pillow 1, bus 2 deflate pillow 1, bus 3 inflate pillow 2, bus 4 deflate pillow 2
    def returnMotor(self, commands):
        commands = commands[::-1]
        motor1 = None
        motor2 = None
        action = None
        time = None

        values = self.getDictValues("FunctionOff")
        for value in values:
            try:
                commands.index(value)
                MC.stopAll()
                return 0
            except ValueError:
                continue

        values = self.getDictValues("Functions")
        for i, value in enumerate(values):
            try:
                commands.index(value)
                action = value
                break
            except ValueError:
                if i == len(values)-1:
                    raise InvalidActionError("Keyword Not Found")
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

        values = self.getDictValues("Pillow1")
        for i, value in enumerate(values):
            try:
                leftIndex = commands.index(value)
            except:
                continue

        values = self.getDictValues("Pillow2")
        for i, value in enumerate(values):
            try:
                rightIndex = commands.index(value)
            except:
                continue

        values = self.getDictValues("PillowAll")
        for i, value in enumerate(values):
            try:
                bothIndex = commands.index(value)
            except:
                continue

        if not bothIndex and not leftIndex and not rightIndex:
            raise InvalidActionError("Pillow assignment unknown")

        if bothIndex < leftIndex and bothIndex < rightIndex:
            continue
        elif leftIndex < rightIndex:
            motor2 = None
        else:
            motor1 = motor2
            motor2 = None

        values = self.getDictValues("TimeAmount")
        for i, value in enumerate(values):
            try:
                commands.index(value)
# fix to set correct number
                Time = value
            except:
                if i == len(values)-1:
                    raise InvalidActionError("Keyword Not Found")
                continue

        values = self.getDictValues("TimeUnits")
        for i, value in enumerate(values):
            try:
                commands.index(value)
                if i == 1:
                    time = time * 60
            except:
                if i == len(values)-1:
                    raise InvalidActionError("Unit of Time Not Found")
                continue
        #time
        #units
        return [motor1, motor2, time]

class InsufficientCommandLengthError(Exception):
    '''Catch the lack of required arguments for a command'''

    def __init__(self, message):
        super().__init__(message)


class KeywordNotFoundError(Exception):
    '''Catch a keyword that does not exist'''

    def __init__(self, message):
        super().__init__(message)


class InvalidActionError(Exception):
    '''Catch an invalid function the pillow needs to inflate or deflate'''

    def __init__(self, message):
        super().__init__(message)


class NonexistentPillowError(Exception):
    '''Catch a pillow that does not exist'''

    def __init__(self, message):
        super().__init__(message)





def text2int(textnum, numwords={}):
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