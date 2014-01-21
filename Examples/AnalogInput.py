#!/usr/bin/env python
import sys

galileo_path = "/media/mmcblk0p1/";
if galileo_path not in sys.path:
    sys.path.append(galileo_path);

from galileo import *

'''/*
  Analog Input
 Demonstrates analog input by reading an analog sensor on analog pin 0 and
 turning on and off a light emitting diode(LED)  connected to digital pin 13. 
 The amount of time the LED will be on and off depends on
 the value obtained by analogRead(). 
 
 The circuit:
 * Potentiometer attached to analog input 0
 * center pin of the potentiometer to the analog pin
 * one side pin (either one) to ground
 * the other side pin to +5V
 * LED anode (long leg) attached to digital output 13
 * LED cathode (short leg) attached to ground
 
 * Note: because most Arduinos have a built-in LED attached 
 to pin 13 on the board, the LED is optional.
 
 
 Created by David Cuartielles
 modified 30 Aug 2011
 By Tom Igoe
 
 This example code is in the public domain.
 
 http:#arduino.cc/en/Tutorial/AnalogInput
 
 */
'''
sensorPin = A0;    # select the input pin for the potentiometer
ledPin = 13;      # select the pin for the LED
sensorValue = 0;  # variable to store the value coming from the sensor

def setup():
  # declare the ledPin as an OUTPUT:
  pinMode(ledPin, OUTPUT);  


def loop():
  global sensorValue;
  # read the value from the sensor:
  sensorValue = analogRead(sensorPin);    
  # turn the ledPin on
  digitalWrite(ledPin, HIGH);  
  # stop the program for <sensorValue> milliseconds:
  delay(sensorValue);          
  # turn the ledPin off:        
  digitalWrite(ledPin, LOW);   
  # stop the program for for <sensorValue> milliseconds:
  print("sensorValue:" + str(sensorValue));
  delay(sensorValue);                  

  #When the file is run from the command line, this fucntion will execute.
#This function just calls setup once, then calls loop over and over. 
if __name__ == "__main__":
    
    setup();
    while(1):
        loop();
