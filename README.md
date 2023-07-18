# MidiToKey
A quick and dirty program that I made to play games with my Midi keyboard.
It can be used for macros, and key combinations.

Add keybinds by pressing esc after entering your Midi device, and typing ` keybinds -note `.
A list of key codes can be found here: https://github.com/boppreh/keyboard

## Linux
on linux pygame and keyboard need to be installed as sudo, even if you have already installed the packages before. this is only a requirement on linux because keyboard needs root access to function on linux.
```sh
sudo pip3 install pygame
sudo pip3 install keyboard
```

if you are getting the error that alsa.conf cannot be found, here is a list of things you can try to fix the issue.

1.try installing the libsound2 package

```sh
sudo apt-get install libasound2
```

2.if you get the message that libsound2 is already installed and up to date, try reinstalling the package

```sh
sudo apt-get install --reinstall libasound2 libasound2-data libasound2-plugins
```

3.if all else fails you migh have to link the alsa.conf file to the directory that is being searched. this command worked for me, but your directories might be different.

```sh
 ln -s /usr/local/share/alsa/alsa.conf /usr/share/alsa/alsa.conf
```
