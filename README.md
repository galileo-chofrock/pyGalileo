pyGalileo
=========

Python library for Intel's Galileo board

How to use:
1. You will need a micro SD card with a Linux image on it: 
    - Format the SD card with a file system of FAT or FAT32.
    - Copy the Linux image onto the card 
        - Download from: http://downloadmirror.intel.com/23171/eng/LINUX_IMAGE_FOR_SD_Intel_Galileo_v0.7.5.7z

2. Download this repository from the git server.
    - https://github.com/galileo-chofrock/pyGalileo

3. Copy the files onto an SD card.
    - Make sure you put the galileo directory in the top level of the SD card.

4. Place the SD card in the Galileo and boot up the system.

5. Connect to the Galileo Linux (via serial console or ssh)
    - Several methods are documented here: https://communities.intel.com/thread/46335

6. Run the examples.
    - /media/mmcblk0p1/galileo/Examples/blink.py

    
To get started developing your own scripts, you can look at the HowToDevelop.txt file in this repository. 