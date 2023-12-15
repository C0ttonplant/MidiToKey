#!/bin/bash

test -d /usr/local/share/alsa

if ($? == 1)
{
    sudo mkdir /usr/local/share/alsa/
    sudo ln -s /usr/local/share/alsa/alsa.conf /usr/share/alsa/alsa.conf
}

/bin/python3 ./MidiToKey.py
