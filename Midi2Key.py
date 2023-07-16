
import os
import sys
import platform

if os.geteuid() != 0 and platform.system() == 'Linux':
    os.execvp('sudo', ['sudo', 'python3'] + sys.argv)

from functools import cmp_to_key
import pygame
import pygame.midi
import keyboard
import json

def main():
    global Device
    global DeviceID
    global InputMode
    global MidiObj

    inp = input(">")
    inp = inp.__str__().lower()
    if inp == 'help':
        print('''Here is a list of commands:

Input:   change the midi input
KeyBind: add or remove keyBinds
Export:  export the current keyBinds
Import:  import keyBinds from a file
List -[arg]: [devices]: lists the midi devices
             [keybinds]: lists the keybinds''')
    elif inp == 'input': #TODO fix error input
        DeviceID = -1
        printMidiDevices()

        while DeviceID == -1:
            inp = input("\nType the device you want to use(case sensitive): ")
            DeviceID = getDeviceIdByName(bytes(inp, "UTF-8", ""), 1)

            if DeviceID == -1:
                print("Invalid name.")
            else:
                Device = pygame.midi.Input(DeviceID)

        print("Success!\n")
    elif inp == 'keybind':
        k = input("Add keybinds by typing a tuple in the form: Note, key.\nLeaving a key blank removes the keybind\n>").strip().lower()
        while True:
            if k == "-1":
                InputMode = True
                print("Quitting text input mode...")
                break
            
            if not k.__contains__(","):
                k = "-1,-1"

            n = k.split(",")[0].strip()
            b = k.split(",")[1].strip() 

            #print(f"[\"{n}\", \"{b}\"]")
            
            if n == "-1" and b == "-1" or n == "":
                k = input("Invalid input. Try again!\n>")
            elif int(n) < 0 and int(n) > 127:
                k = input("Note out of range (0 - 127)\n>")
            elif isValidKey(k):
                k = input("Invalid key. Valid key ex: ctrl+s\n>")
            else:
                keybinds.append(keyBind(b, int(n)))
                updateKeyList()
                k = input("Success!\n>")

class keyBind:
    def __init__(self, keys: str, note: int):
        self.keys = keys
        self.note = note
    def __str__(self):
        return self.note.__str__() + " : " + self.keys.__str__()
    def __repr__(self):
        return {'note':self.note, 'keys': self.keys}
    
    def comparator(a, b):
        if a.note > b.note: return 1
        if a.note < b.note: return -1
        if a.keys > b.keys: return 1
        if a.keys < b.keys: return -1
        return 0

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
    global keybinds
    global keyList
    keybinds = sorted(keybinds, key=cmp_to_key(keyBind.comparator))
    i = 0
    n = 0
    for k in keyList:
        if keybinds[i].note == n:
            keyList[n] = keybinds[i].keys
            if(i < keybinds.__len__() - 1):
                i += 1
        n += 1

def printMidiDevices() -> None:
    i = 0
    print('These are the Midi devices avalable:\n')
    while i < pygame.midi.get_count():
        De = pygame.midi.get_device_info(i)
        if De[2] == 1:
            print(De)

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


InputMode: bool = True
keybinds: list[keyBind] = [keyBind('enter', 67),keyBind('f', 57), keyBind('g', 59), keyBind('h', 60), keyBind('j', 62), keyBind('left_arrow', 69), keyBind('up_arrow', 70), keyBind('down_arrow', 71), keyBind('right_arrow', 72)]
keyList: list[str] = [''] * 127
DeviceID: int = -1
Device: pygame.midi.Input = pygame.midi.Input(pygame.midi.get_default_input_id())
MidiObj: pygame.midi

clearConsole()
print("Welcome to Midi2Key for linux/mac! press ESC to enter text input mode.\n")

updateKeyList()

#display = pygame.display.set_mode((300, 300))

MidiObj = pygame.midi.init()

if(pygame.midi.get_count() == 0):
    print("No midi devices! Quitting...")
    pygame.midi.quit()
    pygame.quit()
    sys.exit()

printMidiDevices()

while DeviceID == -1:
    inp = input("\nType the device you want to use(case sensitive): ")

    DeviceID = getDeviceIdByName(bytes(inp, "UTF-8", ""), 1)
    if DeviceID == -1:
        print("Invalid name.")
    else:
        Device = pygame.midi.Input(DeviceID)

print("Sucsess!\n")

while True:
     
    #handle midi input
    output = pygame.midi.Input.read(Device, 1)
    if keyboard.is_pressed('esc'):
        print("Type help for a list of commands! type -1 to quit.\n")
        InputMode = False

    if output != [] and InputMode:
        print(f"Note: {output[0][0][1]} | Vel: {output[0][0][2].__str__().ljust(3)} | Time: {output[0][1]}")
        for o in output:
            for k in keybinds:
                if keyList[o[0][1]] != '' and o[0][2] != 0:
                    keyboard.press(keyList[o[0][1]])
                elif keyList[o[0][1]] != '':
                    keyboard.release(keyList[o[0][1]])
    if not InputMode:
        main()

    #get async console input

    


pygame.midi.quit()