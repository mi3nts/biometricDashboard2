# CODE TO MAKE EEG ARRAY

# CODE AUTHORED BY: SHAWHIN TALEBI

import matplotlib.pyplot as plt
import numpy as np

def EEGArray():
    # define curvature
    a = -0.035

    # define some parabolic functions
    def Para0(u):
        Para0 = 0
        return Para0

    def Para1(u):
        Para1 = -a*np.square(u) + 1
        return Para1

    def Para2(u):
        Para2 = -a*np.square(u) + 2
        return Para2

    def Para3(u):
        Para3 = -a*np.square(u) + 3
        return Para3

    def Para3(u):
        Para3 = -a*np.square(u) + 3
        return Para3

    def Para4(u):
        Para4 = a*np.square(u) + 4
        return Para4

    # define some x positions
    u1 = np.linspace(0, 4, 5)
    u2 = np.array([ 0, 1.5, 3.5])
    u3 = np.array([0, 1.5])
    u4 = np.array([5])

    # define node locations
    FP1 = (-u3[1], Para4(-u3[1]))
    FP2 = (u3[1], Para4(u3[1]))
    F3 = (-u1[2], Para2(-u1[2]))
    F4 = (u1[2], Para2(u1[2]))
    C3 = (-u1[2], Para0(-u1[2]))
    C4 = (u1[2], Para0(u1[2]))
    P3 = (-u1[2], -Para2(-u1[2]))
    P4 = (u1[2], -Para2(u1[2]))
    O1 = (-u3[1], -Para4(-u3[1]))
    O2 = (u3[1], -Para4(u3[1]))
    F7 = (-u1[4], Para2(-u1[4]))
    F8 = (u1[4], Para2(u1[4]))
    T7 = (-u1[4], Para0(-u1[4]))
    T8 = (u1[4], Para0(u1[4]))
    P7 = (-u1[4], -Para2(-u1[4]))
    P8 = (u1[4], -Para2(u1[4]))
    FZ = (u1[0], Para2(u1[0]))
    CZ = (u1[0], Para0(u1[0]))
    PZ = (u1[0], -Para2(u1[0]))
    OZ = (u1[0], -Para4(u1[0]))
    FC1 = (-u1[1], Para1(-u1[1]))
    FC2 = (u1[1], Para1(u1[1]))
    CP1 = (-u1[1], -Para1(-u1[1]))
    CP2 = (u1[1], -Para1(u1[1]))
    FC5 = (-u1[3], Para1(-u1[3]))
    FC6 = (u1[3], Para1(u1[3]))
    CP5 = (-u1[3], -Para1(-u1[3]))
    CP6 = (u1[3], -Para1(u1[3]))
    FT9 = (-u4[0], Para1(-u4[0]))
    FT10 = (u4[0], Para1(u4[0]))
    FCZ = (u1[0], Para1(u1[0]))
    AFZ = (u2[0], Para3(u2[0]))
    F1 = (-u1[1], Para2(-u1[1]))
    F2 = (u1[1], Para2(u1[1]))
    C1 = (-u1[1], Para0(-u1[1]))
    C2 = (u1[1], Para0(u1[1]))
    P1 = (-u1[1], -Para2(-u1[1]))
    P2 = (u1[1], -Para2(u1[1]))
    AF3 = (-u2[1], Para3(-u2[1]))
    AF4 = (u2[1], Para3(u2[1]))
    FC3 = (-u1[2], Para1(-u1[2]))
    FC4 = (u1[2], Para1(u1[2]))
    CP3 = (-u1[2], -Para1(-u1[2]))
    CP4 = (u1[2], -Para1(u1[2]))
    PO3 = (-u2[1], -Para3(-u2[1]))
    PO4= (u2[1], -Para3(u2[1]))
    F5 = (-u1[3], Para2(-u1[3]))
    F6 = (u1[3], Para2(u1[3]))
    C5 = (-u1[3], Para0(-u1[3]))
    C6 = (u1[3], Para0(u1[3]))
    P5 = (-u1[3], -Para2(-u1[3]))
    P6 = (u1[3], -Para2(u1[3]))
    AF7 = (-u2[2], Para3(-u2[2]))
    AF8 = (u2[2], Para3(u2[2]))
    FT7 = (-u1[4], Para1(-u1[4]))
    FT8 = (u1[4], Para1(u1[4]))
    TP7 = (-u1[4], -Para1(-u1[4]))
    TP8 = (u1[4], -Para1(u1[4]))
    PO7 = (-u2[2], -Para3(-u2[2]))
    PO8 = (u2[2], -Para3(u2[2]))
    FPZ = (u3[0], Para4(u3[0]))
    CPZ = (u1[0], -Para1(u1[0]))
    POZ = (u2[0], -Para3(u2[0]))
    TP10 = (u4[0], -Para1(u4[0]))

    # define a list object for node sites
    list = [FP1, FP2, F3, F4, C3, C4, P3, P4, O1, O2, F7, F8, T7, T8, P7, P8, FZ, CZ, PZ, OZ,FC1, FC2, CP1, CP2,
            FC5, FC6, CP5, CP6, FT9, FT10, FCZ, AFZ, F1, F2, C1, C2, P1, P2, AF3, AF4, FC3, FC4, CP3, CP4, PO3,
            PO4, F5, F6, C5, C6, P5, P6, AF7, AF8, FT7, FT8, TP7, TP8, PO7, PO8, FPZ, CPZ, POZ, TP10]

    # store node coordinates in lists then convert to numpy array
    x = []
    y = []
    for node in list:
        x.append(node[0])
        y.append(node[1])

    x = np.asarray(x)
    y = np.asarray(y)

    return x, y, list