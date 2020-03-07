import os
from tkinter import *
from tkinter import ttk
from functools import partial
import subprocess

# size of the dashboard pop up window - arbitrary numbers chosen

WINDOW_SIZE = "800x400"

# Tk is some Tkinter object. I found this syntax online.
top = Tk()
top.title('UTD MINTS')
# first button
MultiFreq = ttk.Checkbutton(top, text="Aplha")
MultiFreq.grid(column=0, row=0)
# there are three states to a checkbutton in tkinter
MultiFreq.state(['!alternate'])

# column of the new buttons change by 4 as we move right
MultiZscore = ttk.Checkbutton(top, text="Delta")
MultiZscore.grid(column=4, row=0)
MultiZscore.state(['!alternate'])

ZscoreFreq = ttk.Checkbutton(top, text="Theta")
ZscoreFreq.grid(column=8, row=0)
ZscoreFreq.state(['!alternate'])


# this function checks if the button has been selected. Focus is a state when you click on something and it is highlighted.
# Do not change this function - it is crucial to determining whether a button has been selected


def checkIfSelected(state):
    if(state == ('selected',) or state == ('focus', 'selected')):
        return True
    return False

# main function that deals with everything that happens when a user hits 'run':
# we check if the bash script 'runScripts' exists - if it does, we delete it first.
# We create a new runScripts file each time and then write the shebang '#/bin/bash' to it to start the script.
# command 'sh fileName.sh' runs a bash script. '&' runs multiple scripts concurrently. '\n' makes the cursor go to the next line
# command 'python fileName.py &\n' runs a python file concurrently with the next file and moves the cursor to the next line.


def callback():
    if os.path.exists("runScripts.sh"):
        os.remove("runScripts.sh")
    file_object = open('runScripts.sh', 'w+')
    file_object.write("#/bin/bash\n")
    file_object.write("sh runSendData.sh &\n")
    # print (file_object)
    if (checkIfSelected(MultiFreq.state())):
        print("MultiFreq")
        file_object.write("python MultiFrequencies.py &\n")

    if (checkIfSelected(ZscoreFreq.state())):
        print("ZscoreFreq")
        file_object.write("python Z_Scores_ByFreq.py &\n")

    if (checkIfSelected(video.state())):
        print("video")
        file_object.write("sh videoBash.sh &\n")

    if (checkIfSelected(MultiZscore.state())):
        print("MultiZscore")
        file_object.write("python MultiZscore.py &\n")

    file_object.close()
    subprocess.call("sh runScripts.sh", shell=True)


# creates the 'run' button
# b = Button(top, text="RUN", command=callback, height=2, width=5)
# b.grid(row=40, column=5)

top.mainloop()
sys.exit()
