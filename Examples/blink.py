#!/usr/bin/env python
import sys

galileo_path = "/media/mmcblk0p1/";
if galileo_path not in sys.path:
    sys.path.append(galileo_path);

from galileo import *

'''/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.
 
  This example code is in the public domain.
 */
 '''

#// the setup routine runs once when you press reset:
def setup():
    pinMode(led, OUTPUT);     

def loop():
    digitalWrite(led, HIGH);   #// turn the LED on (HIGH is the voltage level)
    delay(1000);               #// wait for a second
    digitalWrite(led, LOW);    #// turn the LED off by making the voltage LOW
    delay(1000);               #// wait for a second

#When the file is run from the command line, this fucntion will execute.
#This function just calls setup once, then calls loop over and over. 
if __name__ == "__main__":
    led = 13;
    setup();
    while(1):
        loop();