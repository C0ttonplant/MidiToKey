# MidiToKey
A quick and dirty program that I made to play games with my Midi keyboard.
It can be used for macros, and key combinations.

Add keybinds by pressing esc after entering your Midi device, and typing ` keybinds -note ` or type `help` for a list of commands.
A list of key codes can be found here: https://github.com/boppreh/keyboard

## Linux
On linux, the pygame and keyboard packages need to be installed as sudo, even if you have already installed the packages before. This is only a requirement on linux because keyboard needs root access to function on linux.
```sh
pip3 install pygame
pip3 install pyautogui
apt-get install python3-tk python3-dev
```

## Mac/Windows
I dont know how well this program will run on mac and windows, because I dont have access to either, so funcionality may vary.
For windows users, there is already a more comprehensive application that does the same thing called [Midikey2Key](https://midikey2key.de/)
