# WiFlip repository  
All python source files of WiFlip.

WiFlip is an application that communicates with any PPS4 Clone through wifi.  
The main benefit of wiflip is game reprogramming (on Recel System 3 MPU Clones) 
One can also emulate the switch matrix of the pinball or test the pysical switches of the pin one by one.

Miniprinter emulation is available, so that one can modify the non volatile ram. 

Coils can be checked individually.

Replication of the display, on a PC or Mac, allows you for diagnosing the real displays.

Additional protections are available for coils.

# Prerequisites  
## Python libraries  
1. pyqt5==5.15.11

# Make an executable with pyinstaller  
That's as easy as bonjour:  
`pyinstaller wiflip.spec`
# Signing the executable (PC)
All informations collected from there:  
https://gist.github.com/PaulCreusy/7fade8d5a8026f2228a97d31343b335e
> :warning: **Warning**  
> Signing the executable will not prevent Windows smartscreen from complaining harshly about the resulting binary. You also have to get on board with Microsoft's developpers plan. And even if you do, it could still complain.
# Make a Windows installer with innosetup



