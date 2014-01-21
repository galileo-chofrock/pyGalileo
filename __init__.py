#!/usr/bin/env python
'''
    This is the main Galileo python file. It will call sub files and bring
    those functions in so they can be used like Arduino Sketches.  
    
    To use in a script add this to the top of the script file:  
    #!/usr/bin/env python
    from galileo import *

    Galileo python library.

    This file contains the functions needed for basic IO communication with
    the Galileo board. This file has the functions: 

    pinMode(pin, direction)  - Used to set whether a digital pin is used as an input or as an output. 
    digitalWrite(pin, value) - Used to write a 1 or a 0 to a digital pin. 
    digitalRead(pin)         - Used to read the value of a digital pin. 
    analogWrite(pin, value)  - Used to write an analog voltage to the PWM pins.
    analogRead(pin)          - Used to read the analog voltage on an analog pin.
    delay(mSec)              - Used to delay the script.
'''

#import the pin library functions
from GalileoPins import *
_pins = GalileoPins();

from Constants import *

import time

def delay(msTime):
    """
    delay(msTime)
    
    Description:
        Delays the execution of the script for number of milliseconds.
        
    Input:  
        msTime - (int) number of milliseconds to delay
    Returns:
        None
    Example:
        delay(500);   - Delay the script for 500 milliseconds.
    """
    time.sleep(msTime/1000);
    
def micros():
    """
    micros()
    
    Description:
        Returns an integer with the current time in mircoseconds.
        
    Input:
        None
    Returns:
        (int) Current time in microseconds
    Example:
        start = micros();
        #something that you want to time
        end   = micros()
        duration = end - start;
    """
    return int(round(time.time() * 1000000))

def millis():
    """
    millis()
    
    Description:
        Returns an integer with the current time in milliseconds.
        
    Input:
        None
    Returns:
        (int) Current time in milliseconds
    Example:
        start = millis();
        #something that you want to time
        end   = millis()
        duration = end - start;
    """
    return int(round(time.time() * 1000))
    
def pinMode(pin, direction):
    """
    pinMode(pin, direction)
    
    Description:
        Sets up the direction for digital pins
    
    Inputs:
        pin       - (int)The digital pin number sent in as
        direction - (string) The direction of the pin using the reserved words, INPUT or OUTPUT. 
    
    Returns: 
        0  (int) if setup worked, 
        -1 (int) if there was an error. 
    
    example:
        pinMode(13, OUTPUT); - sets up digital pin 13 as an output.
        pinMode( 2, INPUT);  - sets up digital pin 2 as in input. 

    """
    _pins.digitalPins[pin].SetupMode(direction);
    
def digitalWrite(pin, value):
    """
    digitalWrite(pin, value)
    
    Description:
        Used to write a 1 or a 0 to a digital pin.
    
    Inputs:
        pin   - (int)The digital pin number sent in as
        value - (string)The value that is to be driven using the reserved words LOW or HIGH
    
    Returns: 
        0  (int) if setup worked, 
        -1 (int) if there was an error. 
    
    example:
        digitalWrite(13, HIGH); - drives digital pin 13 output to a 1.
        digitalWrite( 2, LOW);  - drives digital pin 2 output to a 0. 
    """
    _pins.digitalPins[pin].SetValue(value);
    
def digitalRead(pin):
    """
    digitalRead(pin)
    
    Description:
        Used to read the value of a digital pin.
    
    Inputs:
        pin - (int)The digital pin number sent in as
    
    Returns: 
        Value of the digital pin (HIGH or LOW)
    example:
        val = digitalRead(13); - reads the digital value on pin 13
        val = digitalRead( 2); - reads the digital value on pin 2
    """
    value = _pins.digitalPins[pin].GetValue();
    return value;
    
def analogWrite(pin, value):
    """
    analogWrite(pin, value)
    
    Description:
        Used to write an analog voltage to the PWM pins.
    
    Inputs:
        pin   - (int)The digital pin number (must be a PWM pin)
        value - (int)The value from 0 to 255 that is to be driven out. 
                         0 = 0V
                         255 = 5V
                         which is ~0.196 Volts per integer
    
    Returns: 
        0  (int) if setup worked, 
        -1 (int) if there was an error. 
    
    example:
        analogWrite(9, 10);  - drives digital pin 9 output to almost 0 Volts. 
        analogWrite(3, 255); - drives digital pin 2 output to 5 Volts. 
    """
    _pins.digitalPins[pin].SetPWMValue(value);
    
def analogRead(pin):
    """
    analogRead(pin)
    
    Description:
        Used to read the analog voltage on an analog pin.
    
    Inputs:
        pin       - (string)The Analog pin sent in as a string
    
    Returns: 
        (int) with the value of the pin
        0    = 0 Volts
        1023 = 5 Volts
        ~ 0.004888 Volts per number
        
    example:
        analogRead("A0"); - reads the analog voltage on pin A0
        analogRead("A1"); - reads the analog voltage on pin A1
    """
    num = pin.replace("A", "").replace("a", "");
    value = _pins.analogPins[int(num)].GetValue();
    return value;
   
