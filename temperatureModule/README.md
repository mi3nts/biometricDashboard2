# Temperature Module

A standalone model of the Temperature module -- which can also be found in "Temp Tab" in the main Biometric Dashboard!

______________________________________________________________________________________________________________________________

The Temperature Module has three primary data visualizations - Body Temperature, Galvanic Skin Response and 3-Axis Acceleration. 

______________________________________________________________________________________________________________________________
Need all the files in the same folder: 

    TemperatureModule_Main.py - The entry point to temperature module main window.

	TemperatureModule_BodyTemp.py --- Contains the graph and label widgets for Body Temperature.

    Thermometer.py - Contains the thermometer visualization class.

	TemperatureModule_GSR.py -- Contains the graph and label widgets for Galvanic Skin Response.

	TemperatureModule_Accelerometer.py -- Containts the graph and label widget for 3-Axis Acceleration. 


How to Run this module:

	1) Run SendData.py in a terminal

	2) Run TemperatureModule_Main.py in a different terminal.
  
  
Need Following Python Libraries:
- numpy  (1.18.2 recommended)
- PyQt5  (5.14.2 recommended)
- pyqtgraph (0.10.0 recommended) 
