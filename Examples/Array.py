#!/usr/bin/env python
import sys

galileo_path = "/media/mmcblk0p1/";
if galileo_path not in sys.path:
    sys.path.append(galileo_path);

from galileo import *

'''
/*
  Arrays
 
 Demonstrates the use of  an array to hold pin numbers
 in order to iterate over the pins in a sequence. 
 Lights multiple LEDs in sequence, then in reverse.
 
 Unlike the For Loop tutorial, where the pins have to be
 contiguous, here the pins can be in any random order.
 
 The circuit:
 * LEDs from pins 2 through 7 to ground
 
 created 2006
 by David A. Mellis
 modified 30 Aug 2011
 by Tom Igoe 

This example code is in the public domain.
 
 http://www.arduino.cc/en/Tutorial/Array
 */
'''



def setup():# {
  # the array elements are numbered from 0 to (pinCount - 1).
  # use a for loop to initialize each pin as an output:
  #for (thisPin = 0; thisPin < pinCount; thisPin++):#  {
  for thisPin in range(0,pinCount):
    pinMode(ledPins[thisPin], OUTPUT);      
  #}
#}

def loop():# {
  # loop from the lowest pin to the highest:
  #for (int thisPin = 0; thisPin < pinCount; thisPin++): 
  for thisPin in range(0,pinCount):
    # turn the pin on:
    digitalWrite(ledPins[thisPin], HIGH);   
    delay(timer);                  
    # turn the pin off:
    digitalWrite(ledPins[thisPin], LOW);    

  #}

  # loop from the highest pin to the lowest:
  #for (int thisPin = pinCount - 1; thisPin >= 0; thisPin--): 
  for thisPin in range(pinCount -1, 0, -1):
    # turn the pin on:
    digitalWrite(ledPins[thisPin], HIGH);
    delay(timer);
    # turn the pin off:
    digitalWrite(ledPins[thisPin], LOW);
  #}
#}

if __name__ == "__main__":
    timer = 500;           ## The higher the number, the slower the timing.
    ledPins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 ];## an array of pin numbers to which LEDs are attached
    pinCount = 14;           ## the number of pins (i.e. the length of the array)
    setup();
    while (1):
        loop();