"""HW1 - DATA PLOTTING
Logan Halstrom
MAE 298 AEROACOUSTICS
HOMEWORK 1 - SIGNAL PROCESSING
CREATED: 04 OCT 2016
MODIFIY: 17 OCT 2016

DESCRIPTION: Plot processed signal of sonic boom.
narrow-band spectrum
single-side spectral density
SPL
octave bands
overall SPL
"""

#IMPORT GLOBAL VARIABLES
from hw1_98_globalVars import *

import numpy as np
import pandas as pd

import os

#CUSTOM PLOTTING PACKAGE
import matplotlib.pyplot as plt
import sys
sys.path.append('/Users/Logan/lib/python')
from lplot import *
from seaborn import color_palette
import seaborn as sns
UseSeaborn('xkcd') #use seaborn plotting features with custom colors
colors = sns.color_palette() #color cycle
markers = bigmarkers         #marker cycle

MarkerWidth = 2.25

def PlotArrow(ax, x1, y1, x2, y2, label, head1='<', head2='>',
                color='grey', sz=10):
    """Plot an arrow between two given points.  Specify arrowhead type on
    either side (default double-headed arrow).
    ax      --> plot axis object
    x1,y1   --> x,y coordinates of starting point
    x2,y2   --> x,y coordinates of ending point
    label   --> label for legend
    head1,2 --> first and second arrowheads (e.g. '<', '>', 'v', '^')
    color   --> color of arrow
    sz      --> size of arrowheads
    """
    #Plot line connecting two points
    ax.plot([x1, x2], [y1, y2], color=color, label=label)
    ax.plot(x1, y1, color=color, marker=head1, markersize=sz) #1st arrow head
    ax.plot(x2, y2, color=color, marker=head2, markersize=sz) #2nd arrow head
    return ax


def main():
    """input description
    """

    #Make Plot Output Directory
    MakeOutputDir(picdir)

    #LOAD DATA
    df = pd.read_csv('{}/timespec.dat'.format(datadir), sep=' ' )
    powspec = pd.read_csv('{}/freqspec.dat'.format(datadir), sep=' ' )
    params = pd.read_csv('{}/params.dat'.format(datadir), sep=' ' )
    octv3rd = pd.read_csv('{}/octv3rd.dat'.format(datadir), sep=' ' )
    octv = pd.read_csv('{}/octv.dat'.format(datadir), sep=' ' )


    ####################################################################
    ### 1.1 PLOT PRESSURE WAVE #########################################
    ####################################################################

    #PLOT VOLTAGE
    _,ax = PlotStart(None, 'Time (s)', 'Voltage (V)', figsize=[6, 6])
    #Hollow Marker Plot
    ax.plot(df['time'], df['V'],
            #label=lbl, color=clr,
            # linewidth=0,
            marker=markers[0], markevery=500,
            markeredgecolor=colors[0], markeredgewidth=MarkerWidth,
            markerfacecolor="None",
            )
    savename = '{}/1_1_Voltage.{}'.format(picdir, pictype)
    SavePlot(savename)

    #PLOT PRESSURE IN PASCALS
    _,ax = PlotStart(None, 'Time (s)', 'Pressure (Pa)', figsize=[6, 6])
    #Hollow Marker Plot
    ax.plot(df['time'], df['Pa'],
            #label=lbl, color=clr,
            # linewidth=0,
            #marker=markers[0], markevery=500,
            #markeredgecolor=colors[0], markeredgewidth=MarkerWidth,
            #markerfacecolor="None",
            )
    #Plot horizontal arrow marking shock duration
    ax = PlotArrow(ax, params['ti'], params['Pi'], params['tf'], params['Pi'],
                    label='test', head1='<', head2='>', color='grey', sz=7)
    #Plot vertical dashed line at beginning of shock
    ax.plot([params['tf'], params['tf']], [params['Pi'], params['Pf']],
                color='grey', linestyle='--')
    #Put maximum absolute pressure and shock duration in text box
    text = '$P_{{max}}={:.2f}Pa$\n$t_{{Nwave}}={:.4f}s$'.format(
                                                    float(params['Pmax']),
                                                    float(params['tNwave']) )
    TextBox(ax, text, x=0.39, y=0.82, alpha=0.4)

    ax.set_xlim([0.2, 0.7])

    savename = '{}/1_1_Pressure.{}'.format(picdir, pictype)
    SavePlot(savename)

    ####################################################################
    ### 1.2 PLOT POWER SPECTRUM DENSITY ################################
    ####################################################################

    _,ax = PlotStart(None, 'Frequency (Hz)', '$G_{xx}$ ($Pa^2$/$Hz$)', figsize=[6, 6])
    ax.plot(powspec['freq'], powspec['Gxx'],
            marker=markers[0], markevery=1,
            markeredgecolor=colors[0], markeredgewidth=MarkerWidth,
            markerfacecolor="None",
            )
    plt.xlim([0,50])

    savename = '{}/1_2_PowerSpec.{}'.format(picdir, pictype)
    SavePlot(savename)

    _,ax = PlotStart(None, 'Frequency (Hz)', '$G_{xx}$ ($Pa^2$/$Hz$)', figsize=[6, 6])
    ax.plot(powspec['freq'], powspec['Gxx'],
            marker=markers[0], markevery=1,
            markeredgecolor=colors[0], markeredgewidth=MarkerWidth,
            markerfacecolor="None",
            )
    ax.set_xscale('log')
    plt.xlim([0,10000])

    savename = '{}/1_2_PowerSpecLog.{}'.format(picdir, pictype)
    SavePlot(savename)

    ####################################################################
    ### 1.3 PLOT SOUND PRESSURE LEVEL ##################################
    ####################################################################

    _,ax = PlotStart(None, 'Time (s)', 'SPL (dB)', figsize=[6, 6])
    ax.plot(df['time'], df['SPL'],
            marker=markers[0], markevery=500,
            markeredgecolor=colors[0], markeredgewidth=MarkerWidth,
            markerfacecolor="None",
            )

    savename = '{}/1_3_SPLt.{}'.format(picdir, pictype)
    SavePlot(savename)

    _,ax = PlotStart(None, 'Frequency (Hz)', 'SPL (dB)', figsize=[6, 6])
    ax.plot(powspec['freq'], powspec['SPL'],
            marker=markers[0], markevery=500,
            markeredgecolor=colors[0], markeredgewidth=MarkerWidth,
            markerfacecolor="None",
            )
    ax.set_xscale('log')

    savename = '{}/1_3_SPLf.{}'.format(picdir, pictype)
    SavePlot(savename)

    ####################################################################
    ### 2.1 PLOT 1/3 OCTAVE-BAND SPL ###################################
    ####################################################################

    _,ax = PlotStart(None, 'Frequency (Hz)', 'SPL (dB)', figsize=[6, 6])
    ax.plot(octv3rd['freq'], octv3rd['SPL'],
            marker=markers[0], markevery=500,
            markeredgecolor=colors[0], markeredgewidth=MarkerWidth,
            markerfacecolor="None",
            )
    ax.set_xscale('log')

    savename = '{}/2_1_SPLf_octv3rd.{}'.format(picdir, pictype)
    SavePlot(savename)

    ####################################################################
    ### 2.2 PLOT OCTAVE-BAND SPL #######################################
    ####################################################################

    _,ax = PlotStart(None, 'Frequency (Hz)', 'SPL (dB)', figsize=[6, 6])
    ax.plot(octv['freq'], octv['SPL'],
            marker=markers[0], markevery=500,
            markeredgecolor=colors[0], markeredgewidth=MarkerWidth,
            markerfacecolor="None",
            )
    ax.set_xscale('log')

    savename = '{}/2_2_SPLf_octv.{}'.format(picdir, pictype)
    SavePlot(savename)

    ####################################################################
    ### PLOT ALL OCTAVE-BAND SPL #######################################
    ####################################################################

    _,ax = PlotStart(None, 'Frequency (Hz)', 'SPL (dB)', figsize=[6, 6])

    #Plot Overall SPL as Horizontal Line
    xmin = min(powspec['freq'])
    xmax = max(powspec['freq'])
    ax.plot([xmin, xmax], [params['SPL_overall'], params['SPL_overall']],
            label='Ovr', color='black', linestyle='--')

    i = 1
    #Plot Octave-Band
    ax.plot(octv['freq'], octv['SPL'], label='Oct',
            color=colors[i],
            marker=markers[i], markevery=1,
            markeredgecolor=colors[i], markeredgewidth=MarkerWidth,
            markerfacecolor="None",
            )

    i += 1
    #Plot 1/3 Octave-Band
    ax.plot(octv3rd['freq'], octv3rd['SPL'], label='Oct$\\frac{1}{3}$',
            color=colors[i],
            marker=markers[i], markevery=1,
            markeredgecolor=colors[i], markeredgewidth=MarkerWidth,
            markerfacecolor="None",
            )

    #i += 1
    i = 0
    #Plot Narrow-Band
    ax.plot(powspec['freq'], powspec['SPL'], label='Nar',
            color=colors[i],
            )

    ax.set_xscale('log')
    ax.set_xlim([xmin, xmax])
    PlotLegend(ax)

    #Overall SPL text box
    text = '$L_P={0:.2f}$'.format(float(params['SPL_overall']))
    TextBox(ax, text, x=0.55, y=0.94, alpha=0.4)

    savename = '{}/2_SPLf_all.{}'.format(picdir, pictype)
    SavePlot(savename)



if __name__ == "__main__":




    main()
