# Dashboard Module
## Prerequisites
- Python 3.X
- Cognionics data stream

## Setup
After installing python, these packages must be installed as well.
- PyQt5
- pyqtgraph
- matplotlib
- numpy
- pylsl
- scipy

to install these packages use:
- Windows
```
python -m pip install "package name"
```
- Mac OS
```
pip install "package name"
```
## Execution

To execute the dashboard application, ensure that a data stream is active, then either launch the program by double clicking the python file, or in a command prompt/terminal, use this command:
```
py Dashboard_MainModule.py
```
It is important that the Dashboard_MainModule remains in the same directory it was downloaded in, as it must remain in the same folder as the other required python files. It will be easiest to not remove anything from the downloaded directory.


# Submodules
## EEG Module

The EEGModule has 3 primary visualizations which are the scatter plots of a set of EEG electrodes and a corresponding frequency band, Alpha band, Theta band, and Delta band. The module takes the streamed input from the EEG device over a pyLSL stream and uses a fourier transforms on the data, then is converted into a value that can be mapped in a color map. The color values depicted in the graphs correspond to the nodes' values.

## Respiratory Module

The Respiration Module has five primary visualizations - SPO2, Heart Rate, PPG, ECG and Respiration Graph. The modules display the concentration of the oxygen in the blood, rate of the heartbeat, blood volume changes, electrical activity of the heart and the breaths/minute respectively. Both HR and SpO2 widgets also display a label depicting the body’s current condition based on the their values
## Temperature Module

The Temperature Module has three primary data visualizations - Body Temperature, Galvanic Skin Response and 3-Axis Acceleration.
