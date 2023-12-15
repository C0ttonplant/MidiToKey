#!/bin/bash

test -d /usr/local/share/alsa/

if [ $? = 1 ]
then
    sudo ln -s /usr/share/alsa/  /usr/local/share/alsa
fi

test -f /usr/local/lib/alsa-lib/libasound_module_conf_pulse.so

if [ $? = 1 ]
then
    sudo mkdir /usr/local/lib/alsa-lib/
    sudo ln -s /usr/lib/x86_64-linux-gnu/alsa-lib/libasound_module_conf_pulse.so /usr/local/lib/alsa-lib/libasound_module_conf_pulse.so
fi

/bin/python3 ./MidiToKey.py
