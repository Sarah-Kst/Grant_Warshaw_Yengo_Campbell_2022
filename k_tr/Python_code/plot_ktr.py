# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 12:14:08 2021

@author: srhko
"""
import os 
import matplotlib.pyplot as plt

plt.rcParams.update({'font.family': "Arial"})
plt.rcParams.update({'font.size': 14}) 

import pandas as pd

ROOT = os.path.dirname(__file__)

filename = "../sim_output/analysis.xlsx"

filename_abs = []

for elmt in filename:
    
    filename_abs.append(os.path.join(ROOT, "..", "sim_output", elmt))
    
    
fig = plt.figure(constrained_layout=True, figsize=(4, 4), dpi = 200)
spec = fig.add_gridspec(1, 1)


color_set = ["#0033a0", "#a0001b", "k"]

marker_symbol = ["o", "s", "v"]

ax = []

ax0 = fig.add_subplot(spec[0,0])

ax = [ax0]
  
        
for i in range(1):
    
    ax[i].spines['top'].set_visible(False)
    ax[i].spines['right'].set_visible(False)
    #ax[i].spines['bottom'].set_visible(False)
    #ax[i].set_xticks([])    
    #ax[i].set_xlim(-0.01,  0.9)
    
    for axis in ['top','bottom','left','right']:
        ax[i].spines[axis].set_linewidth(1.5)
        
    for tick in ax[i].yaxis.get_major_ticks():
        tick.label.set_fontsize(14) 
        
    ax[i].tick_params(direction = "out", length = 6, width = 1.5)

ax[0].spines['bottom'].set_visible(True)
ax[0].invert_xaxis()

legend_label = ["model_poly", "model_load", "model_load_wall"]

for j in range(3):
        
    full_data = pd.read_excel(filename)
    
    pd_data = full_data.loc[full_data["curve"] == j+1]
    
    
    ax[0].plot('hs_pCa', 'hs_ktr', data = pd_data, color = color_set[j], linewidth = 1.2, linestyle = "-", marker = marker_symbol[j], markersize = 8, label = legend_label[j]) 
    
    ax[0].set_ylabel("k$\mathregular{_{tr}}$ (s$\mathregular{^{-1}}$)", rotation = 90, labelpad = 20)
    
    ax[0].legend()
    ax[0].set_xlabel('pCa')

