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
        #get correct action
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

        values = self.getDictValues("Pillow")
        for i, value in enumerate(values):
            try:
                index = commands.index(value)
            except:
                if i == len(values)-1:
                    raise InvalidActionError("Keyword Not Found")
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
