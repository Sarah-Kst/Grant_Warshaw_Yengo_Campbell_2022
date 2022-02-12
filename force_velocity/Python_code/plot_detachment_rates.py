# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 17:25:47 2022

@author: sako231
"""


import os
import json

import numpy as np
from natsort import natsorted
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import pandas

model_list = ["../sim_input/1/model.json", "../sim_input/2/model.json", "../sim_input/3/model.json"]


def get_m_kinetics(model_json_file):
    
    # Extract the myosin kinetics from the json model file 

    with open(model_json_file, 'r') as f:
        mod = json.load(f)
           
    m_kinetics = []
    
    for i, isotype in enumerate(mod["m_kinetics"]): # Get data for each isotype
        
        idx = 0
        
        data_scheme = []
        
        for j, state in enumerate(isotype["scheme"]): # Get kinetic scheme for each state
            
            state_data = {}
                        
            state_data["state_number"] = state["number"]
            state_data["state_type"] = state["type"]
            state_data["extension"] = state["extension"]
            state_data["transition"] = []  # array for the different transitions
                       
            for k, trans in enumerate(state["transition"]): # Get transition data for each new state
                
                trans_data = {}
                
                trans_data["to"] = trans["new_state"]
                trans_data["index"] = idx
                trans_data["rate_type"] = trans["rate_type"]
                trans_data["rate_parameters"] = trans["rate_parameters"]
                
                if state["type"] == 'D' and isotype["scheme"][trans["new_state"] - 1]["type"] == 'A':
                    trans_data["trans_type"] = 'a'
                elif state["type"] == 'A' and isotype["scheme"][trans["new_state"] - 1]["type"] == 'D':
                    trans_data["trans_type"] = 'd'
                elif state["type"] == 'S' and isotype["scheme"][trans["new_state"] - 1]["type"] == 'D':
                    trans_data["trans_type"] = 'srx'
                else:
                    trans_data["trans_type"] = 'x'
                
                idx += 1
                
                state_data["transition"].append(trans_data)
                
            data_scheme.append(state_data)
        
        m_kinetics.append(data_scheme)
                
    return m_kinetics

def calculate_detach_rate_from_m_kinetics(m_kinetics, isotype = 1):
    
    # Extract the rate laws from the kinetic data
       
    stretch = np.arange(-10,10,0.1)    
           
    rate_data = pandas.DataFrame()
    
    rate_data["stretch"] = stretch    

    for j, state in enumerate(m_kinetics[isotype - 1]):

        x_ext = state["extension"]
        
        for new_state in state["transition"]:
            
            # Find the detachment transition
            
            transition = new_state["trans_type"]
            
            if transition == 'd':
                
                trans_type = new_state["rate_type"]
                trans_param = new_state["rate_parameters"]
                                                   
                if trans_type == "poly":
    
                    if len(trans_param) == 4:          
                    
                        rate_trans = [trans_param[0] + trans_param[1] * np.power(x + trans_param[3], trans_param[2]) for x in stretch]
    
                    else:
    
                        rate_trans = [trans_param[0] + trans_param[1] * np.power(x + x_ext, trans_param[2]) for x in stretch]                
    
                elif trans_type == "exp":
    
                    if len(trans_param) == 4: # no wall
                    
                        rate_trans = [trans_param[0] + trans_param[1] * np.exp(-trans_param[2] * (x + trans_param[3])) for x in stretch]
    
                    elif len(trans_param) == 5: # wall
                        
                        rate_trans = [ (x < trans_param[4]) * ( trans_param[0] + trans_param[1] * np.exp(-trans_param[2] * (x + trans_param[3])))  
                                      + (x > trans_param[4]) * 1e4 for x in stretch] 
                                      
                                     
                                                          
                else:
                    raise RuntimeError(f"Transition of type {trans_type} is unknown")
                    
                rate_data["detach_rate"] = rate_trans
                
    return rate_data

def plot_detach_rate_from_model_files(model_files):
    
    # Prepare figure + nice layout
    
    fig = plt.figure(constrained_layout=True, figsize=(4, 4), dpi = 200)
    spec = fig.add_gridspec(1, 1)
    ax = fig.add_subplot(spec[0,0])


    color_set = [ "#a0001bff", "#00297ffd", "#7ea8beff", "#df2935b3"]
 
        
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.5)
        
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(14) 
        
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(14) 
        
    ax.tick_params(direction = "out", length = 6, width = 1.5)

    ax.spines['bottom'].set_visible(True)

    legend_label = ["model_poly", "model_load", "model_load_wall"]
    
    # Plot rates for each model file 
    
    for i, model in enumerate(model_files):
        
        m_kin = get_m_kinetics(model)
        
        rate_data = calculate_detach_rate_from_m_kinetics(m_kin)
        
                
        ax.plot(rate_data["stretch"], rate_data["detach_rate"], color = color_set[i], linewidth = 1.2, linestyle = "-",label = legend_label[i]) 
        
    ax.set_xlabel('CB stretch (nm)', fontsize = 14)
    ax.set_ylabel("Detachment rate (s$\mathregular{^{-1}}$)", rotation = 90, labelpad = 20, fontsize = 14)      
    
    ax.set_ylim(0,500)
    ax.legend()

        
        
plot_detach_rate_from_model_files(model_list)   
    
    