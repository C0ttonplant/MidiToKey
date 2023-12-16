
import os
import sys
import platform
from functools import cmp_to_key
import pygame
import pygame.midi
import pyautogui as keyboard
import pynput
import json
import io
import threading

class MyException(Exception): pass

def checkForInput():
    global Device
    global DeviceID
    global InputMode
    global MidiObj
    
    inp = input(">")
    inp = inp.__str__().lower()

    if inp == 'help':
        print('''Here is a list of commands:

Exit:        go back to midi input
Clear:       clear the console
Input:       change the midi input
KeyBinds -[arg]: [note] add or remove note keyBinds
                 [control] add or remove controller keybinds
Export:      export the current keyBinds
Import:      import keyBinds from a file
List -[arg]: [devices]: lists the midi devices
             [keybinds]: lists the keybinds''') 
    elif inp == 'input':
        DeviceID = -1
        printMidiDevices()

        selectMidiDevice(True)
    elif inp.split(" ")[0] == 'keybinds':
        if inp.split(" ")[1] == '-control':
            k = input("Add controller keybinds by typing a tuple in the form: Note, key.\nLeaving the key blank removes the keybind\n>>").strip().lower()
            while True:


                if not k.__contains__(","):
                    k = "-1,-1"

                n = k.split(",")[0].strip()
                b = k.split(",")[1].strip() 

                #print(f"[\"{n}\", \"{b}\"]")

                if n == "-1" and b == "-1" or n == "":
                    k = input("Invalid input. Try again!\n>>")
                elif int(n) < 0 and int(n) > 256:
                    k = input("Data out of range (0 - 255)\n>>")
                elif isValidKey(k):
                    k = input("Invalid key. Valid key ex: ctrl+s\n>>")
                else:
                    if controlList[tryParseInt(n)] != '':
                        i = 0
                        for bind in controlbinds:
                            if bind.note == tryParseInt(n):
                                controlbinds.pop(i)
                                break
                            i += 1
                    if b != '':
                        controlbinds.append(keyBind(b, int(n)))

                    updateKeyList()
                    k = input("Success!\n>>")
        else:
            k = input("Add note keybinds by typing a tuple in the form: Note, key.\nLeaving the key blank removes the keybind\n>>").strip().lower()
            while True:
                if checkForInterupt(k): break


                if not k.__contains__(","):
                    k = "-1,-1"

                n = k.split(",")[0].strip()
                b = k.split(",")[1].strip() 

                #print(f"[\"{n}\", \"{b}\"]")

                if n == "-1" and b == "-1" or n == "":
                    k = input("Invalid input. Try again!\n>>")
                elif int(n) < 0 and int(n) > 256:
                    k = input("Note out of range (0 - 255)\n>>")
                elif isValidKey(k):
                    k = input("Invalid key. Valid key ex: ctrl+s\n>>")
                else:
                    if noteList[tryParseInt(n)] != '':
                        i = 0
                        for bind in notebinds:
                            if bind.note == tryParseInt(n):
                                notebinds.pop(i)
                                break
                            i += 1
                    if b != '':
                        notebinds.append(keyBind(b, int(n)))

                    updateKeyList()
                    k = input("Success!\n>>")
    elif inp == 'clear':
        clearConsole()
    elif inp == 'export':
        k = input("Type the desired directory for the file. press enter for the default\n>>")
        
        if k == "": saveKeyBinds()
        else: saveKeyBinds(k)        
        print("Keybinds successfully saved!")
    elif inp == 'import':
        while True:
            dir = input("Type the directory of the file. press enter for the default\n>>")


            if dir == "": 
                if loadKeyBinds():
                    print("Keybinds loaded successfully!")
                    break
                print("Default file does not exist. Did you save the file as something else?")
            elif loadKeyBinds(dir):
                print("Keybinds loaded successfully!")
                break
            else: print("The file you specified does not exist.")
    elif inp.split(" ")[0] == 'list':
        if inp.split(" ")[1] == "-devices":
            printMidiDevices()
        elif inp.split(" ")[1] == "-keybinds":
            print("Note:")
            for k in notebinds:
                print(k)
            print("Controller:")
            for k in controlbinds:
                print(k)
        else: print("Invalid operator.")

class KeyBindEncoder(json.encoder.JSONEncoder):
    def default(self, o):
            return o.__dict__

class keyBind:
    def __init__(self, keys: str, note: int):
        self.keys = keys
        self.note = note
    def __str__(self):
        return f"{self.note} | {self.keys}"
    def __repr__(self):
        return {'note':self.note, 'keys': self.keys}
    
    def comparator(a, b):
        if a.note > b.note: return 1
        if a.note < b.note: return -1
        if a.keys > b.keys: return 1
        if a.keys < b.keys: return -1
        return 0
    
    def toJSON(self):
        return {
            'keys' : self.keys,
            'note' : self.note
        }

def JSONEncoder(json: str) -> keyBind:
    print(json)
    return keyBind(json.get('keys'), json.get('note'))

def getDeviceIdByName(name: bytes, IO: int) -> int:
    """name: the name of the device. IO: search for the input(1) / output(0) device.
       returns -1 if there is no match"""

    i = 0
    d = 0
    while i < pygame.midi.get_count():
        d = pygame.midi.get_device_info(i)
        if d[1] == name and d[2] == IO:
            return i
        i += 1 
    return -1

def updateKeyList() -> None:
    global notebinds
    global noteList
    global controlbinds
    global controlList

    notebinds = sorted(notebinds, key=cmp_to_key(keyBind.comparator))
    controlbinds = sorted(controlbinds, key=cmp_to_key(keyBind.comparator))
    
    for k in notebinds:
        noteList[k.note] = k.keys
    for k in controlbinds:
        controlList[k.note] = k.keys

def printMidiDevices() -> None:
    i = 0
    print('These are the Midi devices avalable:\n')
    while i < pygame.midi.get_count():
        De = pygame.midi.get_device_info(i)
        if De[2] == 1:
            print(f"{i}: {De}")

        i += 1 

def isValidKey(key: str) -> bool:
    if keyboard.is_modifier(key): return True
    if key.__len__() == 1: return True
    if key.__contains__('+'):
        s = key.split('+')
        isValid = True
        for k in s:
            isValid = keyboard.is_modifier(k) or k.__len__() == 1
            if not isValid: return False
        return True
    return False
            
def clearConsole() -> None:
    if platform.system() == 'Linux':
        os.system('clear')
    else:
        os.system('cls')

def loadKeyBinds(fileDirectory: str = "./KeyBinds.json") -> bool:
    global notebinds
    global controlbinds

    if not os.path.exists(fileDirectory): return False

    fileData: str
    file = io.open(fileDirectory, "r")
    fileData = file.read() + "\n[]"
    if fileData.__len__() != 0:
        notebinds = json.loads(fileData.splitlines()[0], object_hook=JSONEncoder)
        controlbinds = json.loads(fileData.splitlines()[1], object_hook=JSONEncoder)
        file.close()
        return True
    file.close()
    return False

def saveKeyBinds(fileDirectory: str = "./KeyBinds.json") -> bool:
    global notebinds

    fileData: str
    file = io.open(fileDirectory, "w")
    fileData = KeyBindEncoder().encode(notebinds)
    fileData += "\n"
    fileData += KeyBindEncoder().encode(controlbinds)
    file.write(fileData)
    file.close()
    return True

def tryParseInt(s, base=10, val=None) -> int:
  try:
    return int(s, base)
  except ValueError:
    return -1

def selectMidiDevice(checkInterupt: bool = False):
    global DeviceID
    global Device


    pygame.midi.quit()
    pygame.midi.init()

    end = False
    while not end:
        inp = input("\nType the device number you want to use: ")
        if checkInterupt:
            if checkForInterupt(tryParseInt(inp) + int(not checkInterupt)): break
        
        inp = tryParseInt(inp)

        device_is_valid: bool = inp >= 0 and inp <= pygame.midi.get_count()
        if device_is_valid:
            device_is_valid = pygame.midi.get_device_info(inp)[2] == 1


        if not device_is_valid:
            print("Invalid number.")
        else:
            end = True
            DeviceID = inp
            Device = pygame.midi.Input(DeviceID)

def on_press(key):
    global InputMode
    if key == pynput.keyboard.Key.esc:
        print("Type help for a list of commands! type -1 to go back.\n")
        InputMode = not InputMode

def thread_listener():
    print("im a seperate thread")
    # Collect events until released
    with pynput.keyboard.Listener(
            on_press=on_press) as listener:
        try:
            listener.join()
        except MyException as e:
            print('{0} was pressed'.format(e.args[0]))



def main() -> None:
    global notebinds
    global noteList
    global controlbinds
    global controlList
    global DeviceID
    global Device
    global display
    global InputMode

    loadKeyBinds()

    clearConsole()
    print("Welcome to Midi2Key for linux/mac! press ESC to enter/exit text input mode.\n")


    th = threading.Thread(target=thread_listener, args=[])
    th.start()

    updateKeyList()

    #display = pygame.display.set_mode((300, 300))

    if(pygame.midi.get_count() == 0):
        print("No midi devices! Quitting...")
        pygame.midi.quit()
        pygame.quit()
        th.join()
        sys.exit()

    printMidiDevices()

    selectMidiDevice()

    print("Sucsess!\n")

    while True:
        
        #handle midi input
        
        output = pygame.midi.Input.read(Device, 1)

        if output != [] and InputMode:
            for o in output:
                print(f"Data: {o[0][0].__str__().ljust(3)} | Note: {o[0][1].__str__().ljust(3)} | Vel: {o[0][2].__str__().ljust(3)} | Time: {o[1]}")
        
                if noteList[o[0][1]] != '' and o[0][2] != 0 and o[0][0] == 144:
                    keyboard.keyDown(noteList[o[0][1]])
                elif noteList[o[0][1]] != '' and o[0][0] == 128:
                    keyboard.keyUp(noteList[o[0][1]])
                elif controlList[o[0][1]] != '':
                    keyboard.press(controlList[o[0][1]])
        
        elif not InputMode:
            checkForInput()

        #get async console input

        


    pygame.midi.quit()


MidiObj: pygame.midi = pygame.midi.init()
InputMode: bool = True
notebinds: list[keyBind] = []
noteList: list[str] = [''] * 255
controlbinds: list[keyBind] = []
controlList: list[str] = [''] * 255
DeviceID: int = -1
Device: pygame.midi.Input = pygame.midi.Input(pygame.midi.get_default_input_id())
display: pygame.surface

main()