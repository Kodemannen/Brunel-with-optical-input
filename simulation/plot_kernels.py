"""
            Plots the 3 kernels used for mapping population firing rates to LFP 
"""
import numpy as np
import os
from parameters import ParameterSet
import h5py
import matplotlib.pyplot as plt


def Plot_kernels(network_parameters, ax=0):
    if ax == 0:
        ax = plt.axes()
        single_plot = True
    else:
        single_plot = False

    scalebar=True
    PS = network_parameters
    n_channels = PS.n_channels
    kernel_path = PS.kernel_path

    with h5py.File(kernel_path, "r") as file:
        EX_kernel = file["EX"][:]     # / 1000. to get it in uV
        IN_kernel = file["IN"][:]
        LGN_kernel = file["LGN"][:]

    #ax = plt.axes() ## remove later
    unit = 1    # mV
    space = 1.2

    time = np.linspace(0,200,201)

    ##############
    # Normalize: #
    ##############
    scale = np.max([np.max(abs(EX_kernel)), np.max(abs(IN_kernel)), np.max(abs(LGN_kernel))])

    EX_kernel /= scale
    IN_kernel /= scale
    LGN_kernel /= scale

    for i in range(n_channels):
        ax.plot(EX_kernel[i]  + space*(n_channels-i), color="#4363d8", label="EX" if i==1 else None)
        ax.plot(IN_kernel[i]  + space*(n_channels-i),  color="#f58231", label="IN" if i==1 else None)
        ax.plot(LGN_kernel[i] + space*(n_channels-i), color="k", label="LGN" if i==1 else None)

    ####################
    # Adding scalebar: #
    ####################
    if scalebar:
        posx = time[-1]
        posy = 3.5*space
        barlength = 0.01  # uV
        line = barlength/scale * 1/1000. # barlength uV

        ax.plot([posx,posx],[posy-line/2, posy+line/2], color="k", linewidth=2)
        ax.text(posx + 2,posy-0.1, "$%s \mu V$" % barlength)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    yticks = np.arange(space, (n_channels+1)*space, space)

    ax.yaxis.set_ticks(ticks=yticks)#, labels = np.flip(["Ch. %s" %i for i in range(1,n_channels+1)]))
    ax.yaxis.set_ticklabels(np.flip(["Ch. %s" %i for i in range(1,n_channels+1)]))

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_xlabel("Time (ms)")

    ax.set_title("Kernels")
    ax.legend(loc=4, prop={"size": 12})

    if single_plot:
        plt.savefig(PS.kernel_plot) ### remove
        plt.close()

if __name__=="__main__":
    from parameters import ParameterSet
    network_parameters = ParameterSet("params")
    Plot_kernels(network_parameters)