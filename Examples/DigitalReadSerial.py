#!/usr/bin/env python
import sys

galileo_path = "/media/mmcblk0p1/";
if galileo_path not in sys.path:
    sys.path.append(galileo_path);

from pyGalileo import *

'''/*
  DigitalReadSerial
 Reads a digital input on pin 2, prints the result to the serial monitor 
 
 This example code is in the public domain.
 */
'''

#// digital pin 2 has a pushbutton attached to it. Give it a name:
#int pushButton = 2;
pushButton = 2;

#// the setup routine runs once when you press reset:
#void setup() {
def setup():
  #// initialize serial communication at 9600 bits per second:
  #Serial.begin(9600);
  #// make the pushbutton's pin an input:
  pinMode(pushButton, INPUT);
#}

#// the loop routine runs over and over again forever:
#void loop() {
def loop():
  while(1):
      #// read the input pin:
      #int buttonState = digitalRead(pushButton);
      buttonState = digitalRead(pushButton);
      #// print out the state of the button:
      #Serial.println(buttonState);
      print(buttonState);
      delay(1);        #// delay in between reads for stability
#}

setup();
loop();

