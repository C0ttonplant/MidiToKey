# MidiToKey
A quick and dirty program that I made to play games with my Midi keyboard.
It can be used for macros, and key combinations.

Add keybinds by pressing esc after entering your Midi device, and typing ` keybinds -note ` or type `help` for a list of commands.
A list of key codes can be found here: https://github.com/boppreh/keyboard

## Linux
On linux, the pygame and keyboard packages need to be installed as sudo, even if you have already installed the packages before. This is only a requirement on linux because keyboard needs root access to function on linux.
```sh
sudo pip3 install pygame
sudo pip3 install keyboard
```

if you are getting the error that alsa.conf cannot be found, here is a list of things you can try to fix the issue.

1. Try installing the libsound2 package

```sh
sudo apt-get install libasound2
```

2. If you get the message that libsound2 is already installed and up to date, try reinstalling the package

```sh
sudo apt-get install --reinstall libasound2 libasound2-data libasound2-plugins
```

3. If all else fails you migh have to link the alsa.conf file to the directory that is being searched. this command worked for me, but your directories might be different.

```sh
 sudo ln -s /usr/local/share/alsa/alsa.conf /usr/share/alsa/alsa.conf
```

## Mac/Windows
I dont know how well this program will run on mac and windows, because I dont have access to either, so funcionality may vary.
For windows users, there is already a more comprehensive application that does the same thing called [Midikey2Key](https://midikey2key.de/)
