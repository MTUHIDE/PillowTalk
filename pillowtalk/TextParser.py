import datetime
from MotorControl import *

class TextParser:
    def __init__(self):
        self._dictionary = self.openDictionary()
        if self._dictionary == -1:
            self._dictionary = None
            print("dictionary was not pulled")
        self._MC = MotorControl()

    # return -1 Error opening file
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
                command = words[index + 1 : index + 5]
                print("Command: {0}".format(command))
                print("found keyword '{0}' at index {1} in string '{2}'".format( keyword, index, string))
            except ValueError as e:
                # self.saveString("Keyword:'{0}' not found in '{1}'".format(keyword, string)
                raise KeywordNotFoundError(f"Invalid keyword: index {index} does not exist")
        else:
            command = words

        if len(command) < 3:
            raise InsufficientCommandLengthError(f"Command '{command}' Not Long Enough")
        return command

    # return -1 invalid number
    # return -2 invalid action
    # return -3 invalid inflatable
    # bus 1 inflate pillow 1, bus 2 deflate pillow 1, bus 3 inflate pillow 2, bus 4 deflate pillow 2
    def returnRelay(self, command):
        relay = None
        action = command[0]
        pillow = command[1]
        time = int(command[2])

        if len(command) == 4:
            if command[3] == "minute":
                time = time * 60
        if action == "inflate":
            if pillow == "left" or pillow == "cushion_1":
                relay = 1
            elif pillow == "right" or pillow =="write" or pillow == "cushion_2":
                relay = 3
            else:
                raise NonexistentPillowError(f"Pillow {pillow} does not exist")
        elif action == "deflate":
            if pillow == "left" or pillow == "cushion_1":
                relay = 2
            elif pillow == "right" or pillow =="write" or pillow == "cushion_2":
                relay = 4
            else:
                raise NonexistentPillowError(f"Pillow {pillow} does not exist")
        else:
            raise InvalidActionError(f"Action '{action}' is invalid")

        return [relay, time]

    
    # return -2 command not long enough - not enough arguments provided for a command
    # return -1 keyword not found
    # return -2 invalid action - the function the pillow needs to take to inflate or deflate
    # return -3 invalid inflatable - does a pillow not exist?

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