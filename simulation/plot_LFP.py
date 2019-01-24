import numpy as np
import nest
import time
import os
import matplotlib.pyplot as plt
from parameters import ParameterSet
import h5py
from set_parameters import Set_parameters
import sys

def Plot_LFP(LFP, network_parameters, sim_index, class_label, ax=0):
    if ax == 0:
        ax = plt.axes()
        single_plot = True
    else:
        single_plot = False

    PS = network_parameters
    filename = PS.LFP_plot_path + f"LFP-{sim_index}-{class_label}"
    time = np.linspace(0, PS.simtime, LFP.shape[1])

    scalebar=True
    k = np.shape(LFP)[0]

    unit = 1    # mV
    space = 1.2

    ##############
    # Normalize: #
    ##############
    scale = np.max( [np.max(abs(LFP[i])) for i in range(k)] )
    LFP /= scale

    for i in range(k):
        ax.plot(LFP[i] + space*(k-i), color = "black")


    ####################
    # Adding scalebar: #
    ####################
    if scalebar:
        posx = PS.simtime
        posy = 3.5*space
        barlength = 10  # uV
        line = barlength/scale * 1/1000. # barlength uV

        ax.plot([posx,posx],[posy-line/2, posy+line/2], color="k", linewidth=3)
        ax.text(posx + 2,posy-0.1, "$%s \mu V$" % barlength)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    yticks = np.arange(space, (k+1)*space, space)
    ax.yaxis.set_ticks(ticks=yticks)#, labels = np.flip(["Ch. %s" %i for i in range(1,n_channels+1)]))
    ax.yaxis.set_ticklabels(np.flip(["Ch. %s" %i for i in range(1,k+1)]))

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_xlabel("Time (ms)")

    ax.set_title("LFP")
    #ax.legend(loc=4, prop={"size": 12})

    if single_plot:
        plt.savefig(filename) ### remove
        plt.close()
        #plt.show()
    return ax