#!/usr/bin/env python
import sys

galileo_path = "/media/mmcblk0p1/";
if galileo_path not in sys.path:
    sys.path.append(galileo_path);

from pyGalileo import *

def setup():
  #int 
  pin = 2;
  #unsigned int 
  attempts = 10000;
  
  #// Delay for you to open the Serial Monitor
  delay(5000);
  
  #Serial.begin(9600);
  pinMode(pin, INPUT);
  
  print("Starting the loop...");
  #unsigned long 
  start = micros();
  for i in range(0,attempts +1):
    digitalRead(pin);
  #}
  #unsigned long 
  finish = micros();
  #unsigned long 
  duration_all = finish - start;
  print("Ran digitalRead() " + str(attempts) + " times");
  print("Overall duration: " + str(duration_all) + " microseconds");
  print("One digitalRead() duration (approximate, subject to micros() function limitations): " + str(duration_all/attempts) + " microseconds");
  print("Finished");  
#}
 
#void 
def loop():# {
    pass;
#}

#When the file is run from the command line, this fucntion will execute.
#This function just calls setup once, then calls loop over and over. 
if __name__ == "__main__":
    
    setup();
    while(1):
        loop();