import os
from Constants import *

#there is a bug in the firmware version 0.75
#this varible enables a work around for that bug
waBug075 = True;
#Turn on debug messages
DEBUG    = False;#True;


class GalileoPins:
    """
    GalileoPins - class used for controling Galileos Arduino digital and analog pins
    
    Public Members:
        analaogPins[number] #contains a list of AnalogPin objects that can be used to control the Arduino Analog pins. 
        digitalPins[number] #contains a list of DigitalPin objects that can be used to control the Arduino Digital pins.
        
    Examples:
        #initalize the class
        pins = GalileoPins();
        
        #Setup digital pin 13 as an output: (valid values are OUTPUT or INPUT)
        pins.digitalPins[13].SetValue(OUTPUT);
        
        #Drive digital pin 13 high: (valid values are HIGH or LOW)
        pins.digitalPins[13].SetValue(HIGH);
        
        #Read digital value from pin 13: (return will be either HIGH or LOW)
        val = pins.digitalPins[13].GetValue();
        
        #Drive a Pulse Width Modulation onto digital pin 13 (valid values are 0-255) (0=0Volts, 255=5Volts)
        pins.digitalPins[13].SetPWMValue(value)
        
        #Read analog value from pin A0: (returns value from 0 to 1023) (0=0Volts, 1023=5Volts)
        value = _pins.analogPins[0].GetValue()
    """
    analogPins  = []; #list of all the analog pin objects
    digitalPins = []; #list of all the digital pin objects

    #Digital Pins and Muxes
    _VALIDPINS  = [  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13];
    _PIN2GPIO   = ["50","51","32","18","28","17","24","27","26","19","16","25","38","39"];
    _MUXGPIO    = ["40","41","31","30","00","00","00","00","00","00","42","43","54","55"];
    _MUXDRIVE   = [ "1", "1", "1", "1","00","00","00","00","00","00", "1", "1", "1", "1"];
    _MUX2GPIO   = ["00","00", "1", "0","00","00","00","00","00","00","00","00","00","00"];
    _MUX2DRIVE  = ["00","00", "0", "0","00","00","00","00","00","00","00","00","00","00"];
    #PWM Pins (muxes are same as digital)
    _VALIDPWM   = [3,5,6,9,10,11];
    _PWMDICT    = {'3':"3",'5':"5",'6':"6",'9':"1",'10':"7",'11':"4"};
    #Analog Pins and Muxes
    _ANALOGPINS = ["A0","A1","A2","A3","A4","A5"];
    _ANALGPIO   = ["44","45","46","47","48","49"];
    _ANALOGNUM  = {'A0': '0','A1': '1','A2': '2','A3': '3','A4': '4','A5': '5'};
    _ANAMUXPINS = ["37","36","23","22","21","20"];
    _ANAMUXVAL  = [ '0', '0', '0', '0', '0', '0'];
    _ANAMUX2P   = ["00","00","00","00","29","29"];
    _ANAMUX2V   = ["00","00","00","00", "1", "1"];
    

    
    def __init__(self):
        """
        Initializes the analogPins object and the digitalPins object
        """
        if(DEBUG): print("Entering galileoPins init");

        for analog in self._ANALOGPINS:
            name        = analog;
            number      = int(self._ANALOGNUM[name]);
            gpioPin     = self._ANALGPIO[number];
            muxPin      = self._ANAMUXPINS[number];
            muxValue    = self._ANAMUXVAL[number];
            mux2Pin     = self._ANAMUX2P[number];
            mux2Value   = self._ANAMUX2V[number];
                        
            self.analogPins.append(self.AnalogPin(number, name, gpioPin, muxPin, muxValue, mux2Pin, mux2Value));
            
        if(DEBUG):
            for analog in self.analogPins:
                print("Analog pin " + analog.name + " number " + str(analog._number) + " GPIOpin " + analog._gpioPin + " mux " + analog._muxPin + " value " + analog._muxValue);
            
        for digital in self._VALIDPINS:
            name      = digital;
            gpioPin   = self._PIN2GPIO[name]; #Linux Logical number
            muxPin    = self._MUXGPIO[name];  #_muxPin
            muxValue  = self._MUXDRIVE[name]; #_muxValue
            mux2Pin   = self._MUX2GPIO[name]; #There are some pins that have two muxes, currently we do not work with these pins
            mux2Value = self._MUX2DRIVE[name];#There are some pins that have two muxes, currently we do not work with these pins

            #PWM pin information. 
            if(name in self._VALIDPWM):   
                pwmPin       = self._PWMDICT[str(name)];  
                pwmMuxPin    = self._MUX2GPIO[name];   #the digital pins and pwm pins use the same muxes
                pwmMuxValue  = self._MUXDRIVE[name];   #the digital pins and pwm pins use the same muxes
                pwmMux2Pin   = self._MUX2GPIO[name];   #There are some pins that have two muxes, currently we do not work with these pins
                pwmMux2Value = self._MUX2DRIVE[name];  #There are some pins that have two muxes, currently we do not work with these pins
            else:
                #if this is not a valid PWM pin, we will load the PWM variables with zeros
                pwmPin       = "00";
                pwmMuxPin    = "00";
                pwmMuxValue  = 0;
                pwmMux2Pin   = "00";#There are some pins that have two muxes, currently we do not work with these pins
                pwmMux2Value = 0;   #There are some pins that have two muxes, currently we do not work with these pins
                
            
            self.digitalPins.append(self.DigitalPin(name,gpioPin,muxPin,muxValue,pwmPin,pwmMuxPin,pwmMuxValue,mux2Pin,mux2Value,pwmMux2Pin,pwmMux2Value));

        if(DEBUG):
            for digital in self.digitalPins:
                print("Digital pin " + str(digital.name) + " GPIOpin " + digital._gpioPin + " mux " + digital._muxPin + " value " + digital._muxValue );
                if(digital != "00"): print("    PWM pin " + digital._pwmPin + " PWM mux " + digital._pwmMuxPin + " PWM value " + str(digital._pwmMuxValue));
            
    def __del__(self):
        """
        Calls the destructor for each of the objects in the analogPins and digitalPins lists.
        """
        if(DEBUG): print("Entering galileoPins del");
        for analog in self.analogPins:
            del analog;
        for digital in self.digitalPins:
            del digital;
    
    class _Pins:
        """
        A skeleton class so that I don't have to type these functions multiple times. Used only as inheratance.
        """
        def _ReadFile(self,fullFilename):
            '''
            Created this to reduce typing
            '''
            if(DEBUG):print("Reading from file: " + fullFilename);
            myFile = open(fullFilename, "r");
            readValue = myFile.read().strip();
            myFile.close();
            return readValue;
        
        def _WriteFile(self,fullFilename, value):
            '''
            Created this to reduce typing
            '''
            if(DEBUG):print("Writing file: " + fullFilename + " with value " + value);
            myFile = open(fullFilename, "w"); 
            myFile.write(value); 
            myFile.close();
    
    class DigitalPin(_Pins):
        """
        Public Members:
            name                    #This should be a number from 0 to 13
        Public Functions:
            SetupMode(direction)    #Sets up the pin in a specific direction (valid directions are INPUT or OUTPUT)
            GetValue()              #Reads the digital value on the pin (returns HIGH or LOW)
            SetValue(value)         #Sets the digital value on the pin (valid values are HIGH or LOW)
            SetPWMValue(value)      #Sets the Pulse Width Modulation on the pin (valid values are 0-255)
        """
        '''
        Private Members:
            #Digital Pin information
            #_gpioPin;         #the Linux GPIO logical pin number
            #_muxPin;          #the GPIO pin number for the first mux (if no mux set to "00")
            #_muxValue;        #the value that needs to be driven on the first mux
            #_mux2Pin;         #the GPIO pin number for the second mux (if no mux set to "00")
            #_mux2Value;       #the value that needs to be driven on the first mux
            #file handles for controlling digital pin
            #_drive;           #this needs to be set for 0.7.5 firmware version
            #_direction;       #set to 'in' or 'out'
            #_value;           #set to 1 or 0 
            #PWM pin information. 
            #_pwmPin;          #the GPIO pin logical number
            #_pwmMuxPin;       #the GPIO pin number for the first mux (if no mux set to "00")
            #_pwmMuxValue;     #the value that needs to be driven on the first mux
            #_pwmMux2Pin;      #the GPIO pin muber for the second mux (if no 2nd mux set to "00")
            #_pwmMux2Value;    #The value that the second mux needs to be set to. 
            #file handles for PWM pins.
            #We might need to make these public for the Servo functions to work? 
            #_pwmPeriod;       #This controls the period of the pulse
            #_pwmDuty;         #This controls the duty cycle of the pulse
            #used to keep track if a file handles are open
            self._initialize   #true if self._value file hanler is opne
            #used to keep track if we have exported a GPIO pin
            self._gpioExport   #true if we exported the GPIO pin
            self._muxExport    #true if we exported the GPIO pin for the mux
            self._mux2Export   #true if we exported the GPIO pin for the mux level 2
            self._pwmExport    #true if we exported the GPIO pin for the PWM pin
            self._setStrong    #true if we set the drive strenght for the GPIO pin to strong
        '''
        name = None; 
        def __init__(self,name,gpioPin,muxPin,muxValue,pwmPin="00",pwmMuxPin="00",pwmMuxValue="00",mux2Pin="00",mux2Value="00",pwmMux2Pin="00",pwmMux2Value="00"):
            '''
            Sets up the digital pin object (most of these variables are sent from the GalileoPins class
            '''
            if(DEBUG): print("Entering digitialPins init");
            self.name          = name;
            self._gpioPin      = gpioPin;
            self._muxPin       = muxPin;
            self._muxValue     = muxValue;
            self._mux2Pin      = mux2Pin;
            self._mux2Value    = mux2Value;
            #file handles for controlling digital pin
            self._drive        = None;
            self._direction    = None;
            self._value        = None;
            #PWM pin information. 
            self._pwmPin       = pwmPin;
            self._pwmMuxPin    = pwmMuxPin;
            self._pwmMuxValue  = pwmMuxValue;
            self._pwmMux2Pin   = pwmMux2Pin;
            self._pwmMux2Value = pwmMux2Value;
            #file handles for PWM pins.
            self._pwmPeriod    = None;
            self._pwmDuty      = None;
            #used to keep track if a file handles are open
            self._initialize   = False;  
            #used to keep track if we have exported a GPIO pin
            self._gpioExport   = False;
            self._muxExport    = False;
            self._mux2Export   = False;
            self._pwmExport    = False;
            self._setStrong    = False;
        
        def __del__(self):
            '''
            Destructor for the DigitalPins class. Closes any files if open, unexports any GPIO that we exported
            '''
            if(DEBUG): print("Entering digitialPins del");
            #close the files
            if(self._initialize):
                self._value.close();
                if(self._pwmPin != "00"):
                    self._pwmPeriod.close();
                    self._pwmDuty.close()
            #remove the pin
            if(self._gpioExport):
                self._WriteFile("/sys/class/gpio/unexport", self._gpioPin); 
            #remove the Mux
            if(self._muxExport):
                self._WriteFile("/sys/class/gpio/unexport", self._muxPin);
            #remove the second mux, if it exists
            if(self._mux2Pin != "00"):
                if(self._mux2Export):
                    self._WriteFile("/sys/class/gpio/unexport", self._mux2Pin);
            if(self._pwmPin != "00"):
                if(self._pwmExport):
                    self._WriteFile("/sys/class/pwm/pwmchip0/unexport", self._pwmPin)
        
        def SetupMode(self, direction):
            """
            SetupMode(self,direction)
            
            Inputs:
                direction - the direction for the digital pin (valid values are INPUT or OUTPUT)
                
            Returns:
                nothing
                
            Example:
                #setup digital pin 13 as an Output
                digitalPins[13].SetupMode(OUTPUT)
            """
            #this setup the level one mux, if needed. GPIO number "00" indicates no mux is used.
            if(self._muxPin != "00"):
                self._SetupMux();
            #this setup the level two mux, if needed. GPIO number "00" indicates no mux is used.
            #if(self._mux2Pin != "00"):                
            #    self._Setup2Mux();
            #this setup the PWM, if this is a PWM pin. PWM number "00" indicates this is not a PWM pin.
            if(self._pwmPin != "00"):
                self._SetupPWM();
            #this sets up the GPIO pin for controlling the digital pin
            self._SetupPin(direction);
            #This is a file handle that we will use to drive the value for the digital pin.
            self._value = open("/sys/class/gpio/gpio" + self._gpioPin + "/value", "r+");
            #this keeps track of whether the file handle is open or not
            self._initialize = True;
            
        def _SetupMux(self):
            '''
            Sets up the first level mux
            Inputs:
                none
            Outputs:
                none
            Example:
                This should only be called internally.
            '''
            #Check if the MUX GPIO directory already exists
            if(not (os.path.exists("/sys/class/gpio/gpio" + self._muxPin + "/"))):
                if(DEBUG): print("Turning on MUX for pin: " + str(self.name) + "(GPIO " + self._muxPin + ")" );
                #This should create the Setting value on MUX forGPIO drirectory for the mux
                self._WriteFile("/sys/class/gpio/export", self._muxPin); 
                if(DEBUG):
                    #double check that it worked
                    if(not (os.path.exists("/sys/class/gpio/gpio" + self._muxPin + "/"))):
                        print("Tried to enable the mux for pin " + str(self.name) + " but directory " + "/sys/class/gpio/gpio" + self._muxPin + "/ does not exist");
                self._muxExport = True;
            
            #Set the drive strength
            #this only needs to be done for firmware version 0.7.5
            if(waBug075): 
                if(DEBUG):print("Setting the drive strength to strong");
                self._WriteFile("/sys/class/gpio/gpio" + self._muxPin + "/drive", "strong");
                if(DEBUG):
                    #verify the drive strength. 
                    drive = self._ReadFile("/sys/class/gpio/gpio" + self._muxPin + "/drive");
                    if(drive != "strong"):
                        print("ERROR: Tried to set drive strength to strong for pin " + str(self.name) + " but directory " + "/sys/class/gpio/gpio" + self._muxPin + "/drive returned a value of: " + drive);
                        return -1;
            
            #Make sure the Mux pin is setup as an output
            if(DEBUG): print("Enabling Mux for pin " + str(self.name) + "(GPIO " + self._muxPin + ")" );
            self._WriteFile("/sys/class/gpio/gpio" + self._muxPin + "/direction","out");
            if(DEBUG):
                #Verify that it was set correctly
                direct = self._ReadFile("/sys/class/gpio/gpio" + self._muxPin + "/direction");
                if(direct != "out"):
                    print("ERROR: Tried to set direction to out for pin " + str(self.name) + " but directory " + "/sys/class/gpio/gpio" + self._muxPin + "/direction returned a value of: " + direct);
                    return -1;

            #now drive the Mux pin, the value in MUXDRIVE is the value that needs to be driven. 
            if(DEBUG): print("Setting value on MUX for pin:" + str(self.name) + "(GPIO " + self._muxPin + ") to " + self._muxValue);
            self._WriteFile("/sys/class/gpio/gpio" + self._muxPin + "/value", self._muxValue);
            if(DEBUG):
                #double check the value is correct
                value = self._ReadFile("/sys/class/gpio/gpio" + self._muxPin + "/value");
                if(value != self._muxValue):
                    print("ERROR: Tried to set value for mux for pin " + str(self.name) + " but directory " + "/sys/class/gpio/gpio" + self._muxPin + "/value returned a value of: " + value);
                    return -1;
                    
        def _Setup2Mux(self):
            '''
            Sets up the second level mux
            Inputs:
                none
            Outputs:
                none
            Example:
                This should only be called internally.
            '''
            #Check if the MUX GPIO directory already exists
            if(not (os.path.exists("/sys/class/gpio/gpio" + self._mux2Pin + "/"))):
                if(DEBUG): print("Turning on MUX for pin: " + str(self.name) + "(GPIO " + self._mux2Pin + ")" );
                #This should create the Setting value on MUX forGPIO drirectory for the mux
                self._WriteFile("/sys/class/gpio/export", self._mux2Pin); 
                if(DEBUG):
                    #double check that it worked
                    if(not (os.path.exists("/sys/class/gpio/gpio" + self._mux2Pin + "/"))):
                        print("Tried to enable the mux for pin " + str(self.name) + " but directory " + "/sys/class/gpio/gpio" + self._mux2Pin + "/ does not exist");
                self._mux2Export = True;
            
            #Set the drive strength
            #this only needs to be done for firmware version 0.7.5
            if(waBug075): 
                if(DEBUG):print("Setting the drive strength to strong");
                self._WriteFile("/sys/class/gpio/gpio" + self._mux2Pin + "/drive", "strong");
                if(DEBUG):
                    #verify the drive strength. 
                    drive = self._ReadFile("/sys/class/gpio/gpio" + self._mux2Pin + "/drive");
                    if(drive != "strong"):
                        print("ERROR: Tried to set drive strength to strong for pin " + str(self.name) + " but directory " + "/sys/class/gpio/gpio" + self._mux2Pin + "/drive returned a value of: " + drive);
                        return -1;
            
            #Make sure the Mux pin is setup as an output
            if(DEBUG): print("Enabling Mux for pin " + str(self.name) + "(GPIO " + self._mux2Pin + ")" );
            self._WriteFile("/sys/class/gpio/gpio" + self._mux2Pin + "/direction","out");
            if(DEBUG):
                #Verify that it was set correctly
                direct = self._ReadFile("/sys/class/gpio/gpio" + self._mux2Pin + "/direction");
                if(direct != "out"):
                    print("ERROR: Tried to set direction to out for pin " + str(self.name) + " but directory " + "/sys/class/gpio/gpio" + self._mux2Pin + "/direction returned a value of: " + direct);
                    return -1;

            #now drive the Mux pin, the value in MUXDRIVE is the value that needs to be driven. 
            if(DEBUG): print("Setting value on MUX for pin:" + str(self.name) + "(GPIO " + self._muxPin + ") to " + self._mux2Value);
            self._WriteFile("/sys/class/gpio/gpio" + self._mux2Pin + "/value", self._mux2Value);
            if(DEBUG):
                #double check the value is correct
                value = self._ReadFile("/sys/class/gpio/gpio" + self._mux2Pin + "/value");
                if(value != self._mux2Value):
                    print("ERROR: Tried to set value for mux for pin " + str(self.name) + " but directory " + "/sys/class/gpio/gpio" + self._mux2Pin + "/value returned a value of: " + value);
                    return -1;

        def _SetupPin(self,direction):
            '''
            Sets up the pin 
            Inputs:
                none
            Outputs:
                none
            Example:
                This should only be called internally.
            '''            
            #Enable the output
            #check to see if the GPIO directory for the pin already exists. 
            if(DEBUG):print("Setting up pin " + str(self.name) + "(GPIO" + self._gpioPin + ") for direction " + direction);
            if(not (os.path.exists("/sys/class/gpio/gpio" + self._gpioPin + "/"))):
                if(DEBUG): print("Enabling IO" + str(self.name)+ "(GPIO " + self._gpioPin + ")" );
                #this will create the directory for the GPIO pin
                self._WriteFile("/sys/class/gpio/export", self._gpioPin);
                if(DEBUG):
                    #check that the directory was created
                    if(not (os.path.exists("/sys/class/gpio/gpio" + self._gpioPin + "/"))):
                        print("ERROR: Tried to enable pin " + str(self.name) + " but directory " + "/sys/class/gpio/gpio" + self._gpioPin + "/ does not exist");
                        return -1;
                self._gpioExport = True;
            #set the direction for the GPIO pins. 
            if(direction == OUTPUT):
                if(DEBUG): print("Setting IO" + str(self.name) + "(GPIO " + self._gpioPin + ") direction to out" ); 
                #Set the direction
                self._WriteFile("/sys/class/gpio/gpio" + self._gpioPin + "/direction","out");
                if(DEBUG):
                    #verify the direction was set correctly
                    direct = self._ReadFile("/sys/class/gpio/gpio" + self._gpioPin + "/direction");
                    if(direct != "out"):
                        print("ERROR: Tried to set direction to out for pin " + str(self.name) + " but directory /sys/class/gpio/gpio" + self._gpioPin + "/direction returned a value of: " + direct);
                        return -1;
            elif(direction == INPUT):
                if(DEBUG): print("Setting IO" + str(self.name) + "(GPIO " + self._gpioPin + ") direction to in" ); 
                #set the direction 
                self._WriteFile("/sys/class/gpio/gpio" + self._gpioPin + "/direction","in");
                if(DEBUG):
                    #verify the direction for the GPIO pins
                    direct = self._ReadFile("/sys/class/gpio/gpio" + self._gpioPin + "/direction");
                    if(direct != "in"):
                        print("ERROR: Tried to set direction to in for pin " + str(self.name) + " but directory /sys/class/gpio/gpio" + self._gpioPin + "/direction returned a value of: " + direct);
                        return -1;
                return 0;
            else:
                print("Unrecongnized direction: " + direction);
                return -1;
                        
        def _SetupPWM(self):
            '''
            Sets up the PWM pin
            Inputs:
                none
            Outputs:
                none
            Example:
                This should only be called internally.
            '''            
            #If it is an output, and it is one of the PWM pins then we need to Enable PWM.
            if(DEBUG):print("Setting up PWM for pin " + str(self.name));
            if(not (os.path.exists("/sys/class/pwm/pwmchip0/pwm" + self._pwmPin + "/enable"))):
                if(DEBUG): print("Creating PWM " + self._pwmPin );
                self._WriteFile("/sys/class/pwm/pwmchip0/export", self._pwmPin);
                if(DEBUG):
                    #double check that it worked
                    if(not (os.path.exists("/sys/class/pwm/pwmchip0/pwm" + self._pwmPin + "/enable"))):
                        print("Tried to enable the PWM for pin " + str(self.name) + " but directory /sys/class/pwm/pwmchip0/pwm" + self._pwmPin + "/enable does not exist");
                        return -1; 
                self._pwmExport = True;
            self._WriteFile("/sys/class/pwm/pwmchip0/pwm" + self._pwmPin + "/enable","1");
            if(DEBUG):
                read = self._ReadFile("/sys/class/pwm/pwmchip0/pwm" + self._pwmPin + "/enable");
                if(read != "1"):
                    print("Tried to enable the PWM for pin " + str(self.name) + " but the file /sys/class/pwm/pwmchip0/pwm" + self._pwmPin + "/enable returned a value of: " + read);
                    return -1;
            self._pwmPeriod = open("/sys/class/pwm/pwmchip0/pwm" + self._pwmPin + "/period", "r+");
            self._pwmDuty   = open("/sys/class/pwm/pwmchip0/pwm" + self._pwmPin + "/duty_cycle", "r+");
            return 0;
        
        def GetValue(self):
            """
            GetValue()
            
            Description:
                Used to read the value of a digital pin.
            Inputs:
                none
            Returns: 
                Value of the digital pin (HIGH or LOW)
            example:
                val = digitalPins[13].GetValue(); - reads the digital value on pin 13
            """
            if(DEBUG):print("Reading Digital value on pin " + str(self.name)); 
            value = self._value.read().strip();
            self._value.seek(0);
            if(DEBUG): print("Read Value: [" + value + "]");
            if(value == "1"):
                retVal = "HIGH";
            elif(value == "0"):
                retVal = "LOW";
            else:
                print("Error: Read for digital pin returned a value of :" + value);
                return -1;
            if(DEBUG):print("Reading INPUT on pin " + str(self.name) + " read value " + value + "(" + retVal + ")");
            return retVal;

        def SetValue(self,value):
            """
            SetValue(value)
            
            Description:
                Used to set the value of a digital pin.
            Inputs:
                value - Valid values are (HIGH or LOW)
            Returns: 
                None:
            example:
                digitalPins[13].SetValue(LOW); - sets the digital value on pin 13 to 0.
            """
            #Check Inputs
            if(DEBUG): print("SetValue to: [" + str(value) + "]");
            if(value == HIGH):
                setValue = "1";
            elif(value == LOW):
                setValue = "0";
            else:
                print("Valid values are only HIGH and LOW\n");
                return -1;

            #There is a bug in the 0.7.5 firmware that requires the drive value to be set to strong
            if(waBug075 and (self._setStrong == False)): 
                #Set the drive strength
                if(DEBUG):print("setting the drive strength to strong");
                self._WriteFile("/sys/class/gpio/gpio" + self._gpioPin + "/drive","strong");
                if(DEBUG):
                    #verify the drive strength. 
                    drive = self._ReadFile("/sys/class/gpio/gpio" + self._gpioPin + "/drive");
                    if(drive != "strong"):
                        print("ERROR: Tried to set drive strength to strong for pin " + str(self.name) + " but directory /sys/class/gpio/gpio" + self._gpioPin + "/drive returned a value of: " + drive);
                        return -1;
                    self._setStrong = True;

            if(DEBUG):print("Setting ouput on pin " + str(self.name) + " with value " + str(value) + "(" + setValue + ")");
            #write the value to the file
            self._value.write(setValue);
            #set the pointer for the file back to the begining of the file 
            self._value.seek(0);
            if(DEBUG):
                #verify that the value was set
                value = self._value.readline().strip();
                if(DEBUG): print("Read value: [" + value +"]");
                #set the pointer for the file back to the begining of the file 
                self._value.seek(0);
                if(value != setValue):
                    print("ERROR: Tried to set value to " + setValue + " for pin " + str(self.name) + " but directory /sys/class/gpio/gpio" + self._gpioPin + "/value returned a value of: " + value);
                    return -1;
            return 0;

        def SetPWMValue(self,value):
            """
            SetPWMValue(value)
            
            Description:
                Used to set the value of a digital pin using Pulse Width Modulation (PWM)
            Inputs:
                value - (int)Valid values are 0-255
            Returns: 
                None:
            example:
                digitalPins[13].SetValue(LOW); - sets the digital value on pin 13 to 0.
            """            
            PERIOD = 1000000;
            if(((value < 0) or (value > 255))):
                print("Valid values are between 0 and 255.\n");
                return -1;
            dutyCycle = int(round(((PERIOD*value)/255),0));
            if(DEBUG): print("Duty Cycle: " + str(dutyCycle) + " Value: " + str(value) + " Percentage:" + str(round((dutyCycle/PERIOD)*100 ,0)));
            
            #we need to turn off the digital driver for this pin so the PWM drive will work
            self._value.write("0");
            #self._value.close();
            #There is a bug in the 0.7.5 firmware that requires the drive value to be set to strong
            '''if(waBug075): 
                #Set the drive strength
                if(DEBUG):print("setting the drive strength to strong");
                self._WriteFile("/sys/class/gpio/gpio" + self._gpioPin + "/drive"," ");
                if(DEBUG):
                    #verify the drive strength. 
                    drive = self._ReadFile("/sys/class/gpio/gpio" + self._gpioPin + "/drive");
                    if(drive != " "):
                        print("ERROR: Tried to set drive strength to nothing for pin " + str(self.name) + " but directory /sys/class/gpio/gpio" + self._gpioPin + "/drive returned a value of: " + drive);
                        return -1;
            '''
            '''if((os.path.exists("/sys/class/gpio/gpio" + self._gpioPin + "/"))):
                if(DEBUG): print("Disabling IO " + str(self.name) + "(GPIO " + self._gpioPin + ")" );
                self._WriteFile("/sys/class/gpio/unexport", self._gpioPin);
                if(DEBUG):
                    #check that the directory was created
                    if((os.path.exists("/sys/class/gpio/gpio" + self._gpioPin + "/"))):
                        print("ERROR: Tried to disable pin " + str(self.name) + " but directory " + "/sys/class/gpio/gpio" + self._gpioPin + "/ STILL exists");
                        return -1;            
            '''
            #Set the Period of the Pulse
            self._pwmPeriod.write(str(PERIOD));
            self._pwmPeriod.seek(0);
          
            #verify period is set correctly
            if(DEBUG):
                read = self._pwmPeriod.readline().strip();
                self._pwmPeriod.seek(0);
                if(int(read) != PERIOD):
                    print("ERROR: Tried to set period for PWM pin " + str(self.name) + " but directory /sys/class/pwm/pwmchip0/pwm" + self._pwmPin + "/period returned a value of: (" + read + ")");
                    return -1;

            #Set the Duty Cycle for the pulse
            self._pwmDuty.write(str(dutyCycle));
            self._pwmDuty.seek(0);
            #verify duty Cycle is set correctly
            if(DEBUG):
                read = self._pwmDuty.readline().strip();
                self._pwmDuty.seek(0);
                if(int(read) != dutyCycle):
                    print("ERROR: Tried to set duty cycle for PWM pin " + str(self.name) + " but directory /sys/class/pwm/pwmchip0/pwm" + self._pwmPin + "/duty_cycle returned a value of: " + read);
                    return -1;
            return 0;

        def __str__(self):
            return str(self.name);
            
    class AnalogPin(_Pins):
        """
        Public Members:
            name                    #This should be a string valid values are [A0,A1,A2,A3,A4,A5]
        Public Functions:
            GetValue()              #Reads the analog value on the pin (returns (int) 0-255)
        """
        name        = None;
        _initialize = False;

        def __init__(self, number, name, gpioPin, muxPin="00", muxValue="0", mux2Pin="00", mux2Value="0"):
            '''
            Initalizes the values for the member variables. Most of these are passed in from the GalileoPins class.
            '''
            if(DEBUG): print("Entering analogPins init");
            self.name       = name;         #(string)The name of the digital pin ie("A0")
            self._number    = number;       #(int)the number of the analog pin 
            self._gpioPin   = gpioPin;      #(string)The Linux Logical GPIO pin used to access analog pin
            self._muxPin    = muxPin;       #(string)The Linux Logical GPIO pin for the first level mux
            self._muxValue  = muxValue;     #(string)The drive vaue for the first level mux
            self._mux2Pin   = mux2Pin;      #(string)The Linux Logical GPIO pin for the second level mux
            self._mux2Value = mux2Value;    #(string)The drive vaue for the first level mux
            self._initialize = False;       #(bool)Whether the analog pin has been setup
            self._gpioExport = False;       #(bool)Whether Linux Logical GPIO pin has been setup
            self._muxExport  = False;       #(bool)Whether Linux Logical GPIO pin for the first level mux has been setup
            self._mux2Export = False;       #(bool)Whether Linux Logical GPIO pin for the first second mux has been setup
        
        def __del__(self):
            '''
            Destructor for the AnalogPins class. Closes any files if open, unexports any GPIO that we exported.
            '''
            if(DEBUG): print("Entering analogPins del");
            #remove the pin
            if(self._gpioExport):
                self._WriteFile("/sys/class/gpio/unexport", self._gpioPin); 
            #remove the Mux
            if(self._muxExport):
                self._WriteFile("/sys/class/gpio/unexport", self._muxPin);
            #remove the second mux, if it exists
            if(self._mux2Pin != "00"):
                if(self._mux2Export):
                    self._WriteFile("/sys/class/gpio/unexport", self._mux2Pin);
            #Close the file handle for the value
            if(self._initialize):
                self._value.close();
       
        def _SetupMux(self):
            '''
            Sets up the first level mux
            Inputs:
                none
            Outputs:
                none
            Example:
                This should only be called internally.
            '''
            #check to see if the GPIO directory for the mux already exists. 
            if(not (os.path.exists("/sys/class/gpio/gpio" + self._muxPin + "/"))):
                if(DEBUG): print("Enabling Mux for " + str(self.name) + "(GPIO " + self._muxPin + ")" );
                #this will create the directory for the GPIO pin
                self._WriteFile("/sys/class/gpio/export", self._muxPin);
                if(DEBUG):
                    #check that the directory was created
                    if(not (os.path.exists("/sys/class/gpio/gpio" + self._muxPin + "/"))):
                        print("ERROR: Tried to enable pin " + str(self.name) + " but directory " + "/sys/class/gpio/gpio" + self._muxPin + " does not exist");
                        return -1;
            self._muxExport = True;
            #There is a bug in the 0.7.5 firmware that requires the drive value to be set to strong
            if(waBug075): 
                #Set the drive strength
                if(DEBUG):print("setting the drive strength to strong");
                self._WriteFile("/sys/class/gpio/gpio" + self._muxPin + "/drive","strong");
                if(DEBUG):
                    #verify the drive strength. 
                    drive = self._ReadFile("/sys/class/gpio/gpio" + self._muxPin + "/drive");
                    if(drive != "strong"):
                        print("ERROR: Tried to set drive strength to strong for pin " + str(self.name) + " but directory " + "/sys/class/gpio/gpio" + self._muxPin + "/drive returned a value of: " + drive);
                        return -1;
            #set the direction for the GPIO pins. 
            if(DEBUG): print("Setting Mux for IO" + str(self.name) + "(GPIO " + self._muxPin + ") direction to out" ); 
            #Set the direction
            self._WriteFile("/sys/class/gpio/gpio" + self._muxPin + "/direction","out");
            if(DEBUG):
                #verify the direction was set correctly
                direct = self._ReadFile("/sys/class/gpio/gpio" + self._muxPin + "/direction");
                if(direct != "out"):
                    print("ERROR: Tried to set direction to out for pin " + str(self.name) + " but directory /sys/class/gpio/gpio" + self._muxPin + "/direction returned a value of: " + direct);
                    return -1;
            if(DEBUG): print("Setting value on MUX for pin:" + str(self.name) + "(GPIO " + self._muxPin + ") to " + self._muxValue);
            #now drive the Mux pin, the value in MUXDRIVE is the value that needs to be driven. 
            self._WriteFile("/sys/class/gpio/gpio" + str(self._muxPin) + "/value",self._muxValue);
            if(DEBUG):
                #double check the value is correct
                value = self._ReadFile("/sys/class/gpio/gpio" + self._muxPin + "/value");
                if(value != self._muxValue):
                    print("ERROR: Tried to set value for mux for pin " + str(self.name) + " but directory " + "/sys/class/gpio/gpio" + self._muxPin + "/value returned a value of: " + value);
                    return -1;
        
        def _Setup2Mux(self):
            '''
            Sets up the second level mux
            Inputs:
                none
            Outputs:
                none
            Example:
                This should only be called internally.
            '''
            if(self._mux2Pin!="00"):
                if(not (os.path.exists("/sys/class/gpio/gpio" + self._mux2Pin + "/"))):
                    if(DEBUG): print("Enabling IO " + str(self.name) + "(GPIO " + self._mux2Pin + ")" );
                    #this will create the directory for the GPIO pin
                    self._WriteFile("/sys/class/gpio/export",self._mux2Pin);
                    if(DEBUG):
                        #check that the directory was created
                        if(not (os.path.exists("/sys/class/gpio/gpio" + self._mux2Pin+ "/"))):
                            print("ERROR: Tried to enable pin " + str(self.name) + " but directory " + "/sys/class/gpio/gpio" + self._mux2Pin + "/ does not exist");
                            return -1;
                self._mux2Export = True; 
                #There is a bug in the 0.7.5 firmware that requires the drive value to be set to strong
                if(waBug075): 
                    #Set the drive strength
                    if(DEBUG):print("setting the drive strength to strong");
                    self._WriteFile("/sys/class/gpio/gpio" + self._mux2Pin + "/drive","strong");
                    if(DEBUG):
                        #verify the drive strength. 
                        drive = self._ReadFile("/sys/class/gpio/gpio" + self._mux2Pin + "/drive");
                        if(drive != "strong"):
                            print("ERROR: Tried to set drive strength to strong for pin " + str(self.name) + " but directory " + "/sys/class/gpio/gpio" + self._mux2Pin + "/drive returned a value of: " + drive);
                            return -1;
                #set the direction for the GPIO pins. 
                if(direction == OUTPUT):
                    if(DEBUG): print("Setting Mux for IO " + str(self.name) + "(GPIO " + self._mux2Pin + ") direction to out" ); 
                    #Set the direction
                    self._WriteFile("/sys/class/gpio/gpio" + self._mux2Pin+ "/direction","out");
                    if(DEBUG):
                        #verify the direction was set correctly
                        direct = self._ReadFile("/sys/class/gpio/gpio" + self._mux2Pin + "/direction");
                        if(direct != "out"):
                            print("ERROR: Tried to set direction to out for pin " + str(self.name) + " but directory /sys/class/gpio/gpio" + self._mux2Pin + "/direction returned a value of: " + direct);
                            return -1;
                    return 0;
                if(DEBUG): print("Setting value on MUX for pin:" + str(self.name) + "(GPIO " + self._mux2Pin + ") to " + self._mux2Value);
                #now drive the Mux pin, the value in MUXDRIVE is the value that needs to be driven. 
                self._WriteFile("/sys/class/gpio/gpio" + str(self._mux2Pin) + "/value",self._mux2Value);
                if(DEBUG):
                    #double check the value is correct
                    value = self._ReadFile("/sys/class/gpio/gpio" + self._mux2Pin + "/value");
                    if(value != self._mux2Value):
                        print("ERROR: Tried to set value for mux for pin " + str(self.name) + " but directory " + "/sys/class/gpio/gpio" + self._mux2Pin + "/value returned a value of: " + value);
                        return -1;
        
        def _Initialize(self):
            '''
            Analog pins do not have a Setup function, so we will need to create one. 
            When an analog pin is accessed for the first time, this fucntion will be called
            '''
            #setup the first level mux if needed. A value of "00" indicates no mux is needed
            if(self._muxPin != "00"):
                self._SetupMux();
            #setup the second level mux if needed. A value of "00" indicates no second level mux is needed
            if(self._mux2Pin != "00"):
                self._Setup2Mux();
            
            #Open a file handle for the value file.
            self._value = open("/sys/bus/iio/devices/iio:device0/in_voltage" + str(self._number) + "_raw","r");
            #boolean to keep track of whether this function has been called yet.
            self._initialize = True;
        
        def GetValue(self):
            """
            GetValue()
            
            Description:
                Used to read the analog voltage on an analog pin.
            Inputs:
                None
            Returns: 
                (int) with the value of the pin
                0    = 0 Volts
                1023 = 5 Volts
                ~ 0.004888 Volts per number
            example:
                #read the value on analog pin "A0"
                val = AnalogPins[0].analogRead();
                #read the value on analog pin "A5"
                val = AnalogPins[5].analogRead();
            """
            #check to verify if the pin has been initialized. 
            if(not (self._initialize)):
                self._Initialize();
            if(DEBUG):print("Reading Analog value on pin " + str(self.name)); 
            #read the value
            value = self._value.read().strip();
            #set the pointer for the file back to the begining of the file 
            self._value.seek(0);
            if(DEBUG):print("Value: [" + value + "]");
            return int(value);

        def __str__(self):
            return self.name;
