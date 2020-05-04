# Respiration Module

This is a standalone model of the Respiration module -- which can also be found in "Resp Tab" in the main Biometric Dashboard!

______________________________________________________________________________________________________________________________

The Respiration Module has five primary visualizations - SPO2, Heart Rate, PPG, ECG and Respiration Graph. The modules display the concentration of the oxygen in the blood, rate of the heartbeat, blood volume changes, electrical activity of the heart and the breaths/minute respectively. Both HR and SpO2 widgets also display a label depicting the body’s current condition based on the their values.

Heart Labels:
  if between 60 - 80 --> "Condition White! -- Normal HR"
  
  if between 81 - 114 --> "Condition Yellow! -- Normal but High HR"
  
  if between 115 - 145 --> "Condition Red! -- Motor Skill Deteriorates"
  
  if between 145 - 175 --> "Condition Black! -- Irational Flight or Flee"
  

Sp02 Labels:
  
  if more than 95% --> "Normal -- Healthy"
  
  if between 85% - 94% --> "Hypoxic"
  
  if less than 85 --> "Severly Hypoxic"
______________________________________________________________________________________________________________________________
Need all the files in one folder including the images: 
RM_Main.py --- Contains the main Respiratory Module
RM_Graphs.py -- Contains all the graphs widgtes (HR, SPo2, ECG, Resp, PPG)
RM_Spo2Widget.py -- Containts the Spo2 Widget. 
RM_HRWidget.py -- Contains the HR Widget.

How to Run:
  1) Run SendData.py in a terminal
  2) Run RM_Main.py in a different terminal.
  
  

