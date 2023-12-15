#!/bin/bash

test -f /usr/local/share/alsa/alsa.conf

if [ $? = 1 ]
then
    sudo mkdir /usr/local/share/alsa/
    sudo ln -s /usr/share/alsa/alsa.conf  /usr/local/share/alsa/alsa.conf
fi

/bin/python3 ./MidiToKey.py
