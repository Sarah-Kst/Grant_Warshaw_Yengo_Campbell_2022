# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 08:14:04 2021

@author: srhko
"""
import os 
import matplotlib.pyplot as plt

plt.rcParams.update({'font.family': "Arial"})
plt.rcParams.update({'font.size': 14}) 

import pandas as pd
import numpy as np
    
from scipy.optimize import curve_fit

ROOT = os.path.dirname(__file__)

    
filename_abs = os.path.join(ROOT, "..", "sim_output", "analysis.xlsx")

pd_data = pd.read_excel(filename_abs)

### fit functions

def fit_hyperbola(x, y):
    """ Fits hyperbola of form (x+a)(y+b) = b*(x_0+a) to y data """
    
    def y_hyperbola(x_data, x_0, a, b):
        y = np.zeros(len(x_data))
        for i,x in enumerate(x_data):
            y[i] = ((x_0+a)*b)/(x+a) - b
        return y
    
    popt, pcov = curve_fit(y_hyperbola, x, y,
                           [np.amax(x), 0.1*np.amax(x), 0.05])
    
    d = dict()
    d['x_0'] = popt[0]
    d['a'] = popt[1]
    d['b'] = popt[2]
    d['x_fit'] = np.linspace(0, np.amax(x), 1000)
    d['y_fit'] = y_hyperbola(d['x_fit'], *popt)
    
    return d

def fit_power_curve(x, y):
    """ Fits power curve of form y = x*b*(((x_0+a)/(x+a))-1) to y data """
    
    def y_power(x_data, x_0, a, b):
        y = np.zeros(len(x_data))
        for i,x in enumerate(x_data):
            y[i] = x*b*(((x_0+a)/(x+a))-1)
        return y
    
    popt, pcov = curve_fit(y_power, x, y,
                           [np.amax(x), 0.1*np.amax(x), 0.05])
    
    d = dict()
    d['x_0'] = popt[0]
    d['a'] = popt[1]
    d['b'] = popt[2]
    d['x_fit'] = np.linspace(0, np.amax(x), 1000)
    d['y_fit'] = y_power(d['x_fit'], *popt)
    
    return d

### FIGURE
    
    
fig = plt.figure(constrained_layout=True, figsize=(6, 6), dpi = 200)
spec = fig.add_gridspec(2, 1, hspace=0, wspace =0, height_ratios = [1,1])


color_set = [ "#a0001bff", "#00297ffd", "#7ea8beff", "#df2935b3"]

ax = []

ax0 = fig.add_subplot(spec[0,0])
ax1 = fig.add_subplot(spec[1,0])


ax = [ax0, ax1]
  
        
for i in range(2):
    
    ax[i].spines['top'].set_visible(False)
    ax[i].spines['right'].set_visible(False)

    
    ax[i].spines['left'].set_position(('data', 0))
    ax[i].spines['bottom'].set_position(('data', 0))
    
    for axis in ['top','bottom','left','right']:
        ax[i].spines[axis].set_linewidth(1.5)
        
    for tick in ax[i].yaxis.get_major_ticks():
        tick.label.set_fontsize(14) 
        
    ax[i].tick_params(direction = "out", length = 6, width = 1.5)

ax[0].set_title("3-state model with MyBPC")


legend_label = ["poly", "load", "load with wall"]
marker_symbol = ["o", "s", "^"]

for j in range(3):
    
    # Filter data
       
    data_curve = pd_data.loc[pd_data["curve"] == j+1]
     
    data_curve['hs_force'] = data_curve['hs_force']/1000 # force in kN/m²
    
    
    #data_curve['hs_force'] = data_curve['hs_force']/max(data_curve['hs_force']) # normalized
    
    
    data_curve['hs_velocity'] = data_curve['hs_velocity']/1.1e-6 # velocity in ML/s
    
    # Fit data points
    
    fit_velocity = fit_hyperbola(data_curve['hs_force'], data_curve['hs_velocity'])
    
    fit_power = fit_power_curve(data_curve['hs_force'], data_curve['hs_power'])

    
    # 1) Force-velocity
    
    ax[0].plot('hs_force', 'hs_velocity', data = data_curve, color = color_set[j], linewidth = 1.2, linestyle = "None", marker = marker_symbol[j],label = legend_label[j], markersize = 8) 
    
    ax[0].plot(fit_velocity["x_fit"], fit_velocity["y_fit"], color = color_set[j], linewidth = 1.2, linestyle = "-")
    

    ax[0].set_ylabel("Shortening velocity (ML $\mathregular{s}^{\mathregular{-1}}}$)", rotation = 90, labelpad = 20)
    ax[0].legend(loc = "upper right")

    
    # 2) Force-power
    
    
    ax[1].plot('hs_force', 'hs_power', data = data_curve, color = color_set[j], linewidth = 1.2, linestyle = "None", marker = marker_symbol[j],label = legend_label[j], markersize = 8) 
    
    ax[1].plot(fit_velocity["x_fit"], fit_power["y_fit"], color = color_set[j], linewidth = 1.2, linestyle = "-")


    ax[1].set_ylabel("Power (W)", rotation = 90)
    ax[1].set_xlabel("Force (kN $\mathregular{m}^{\mathregular{-2}}$)")
    



    
    
    
    



