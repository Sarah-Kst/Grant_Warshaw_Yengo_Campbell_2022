# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 18:08:01 2022

@author: sako231
"""

import os, sys
import pandas as pd
import json

# Prepare batch file

job_file_string = '../batch_k_tr.json'

b = dict()
b['FiberSim_batch'] = dict()
b['FiberSim_batch']["FiberCpp_exe"] = dict()
b['FiberSim_batch']["FiberCpp_exe"]["relative_to"] = "this_file"
b['FiberSim_batch']["FiberCpp_exe"]["exe_file"] = "../../FiberSim/bin/fibercpp.exe"

b['FiberSim_batch']["job"] = []

# Prepare array of jobs

model_list = ["model_poly", "model_load", "model_load_wall"]

pCa_list = [4.5, 5.0, 5.5, 5.6, 5.7, 5.8]


for i, model_file in enumerate(model_list):
    
    i = i + 1
    
    for j, pCa in enumerate(pCa_list):
        
        j = j + 1

        # Create a job for each pCa value 
        d=dict()
        d['relative_to'] = 'this_file'
        d['model_file'] = os.path.join('sim_input', '%i' % i,'model.json')
        d['options_file'] = 'sim_input/sim_options.json'
        d['protocol_file'] = os.path.join('sim_input', '%i' % i, 'protocol_%i.txt' % j)
        d['results_file'] = os.path.join('sim_output', '%i' % i, 'results_%i.txt' % j)
                                         
        d['output_handler_file'] = os.path.join('sim_input', '%i' % i, 'output_handler_%i.json' % j)
    
        # Add job
        
        b['FiberSim_batch']["job"].append(d)
    

# Prepare batch_figures

b['FiberSim_batch']["batch_figures"] = dict()
b['FiberSim_batch']["batch_figures"]["ktr"] = []

# ktr-force curve

analysis = dict()

analysis["relative_to"] = "this_file"
analysis["results_folder"] = "sim_output"
analysis["data_field"] = "force"
analysis["output_data_file_string"] = "sim_output/analysis.xlsx"
analysis["output_image_file_string"] = "sim_output/ktr_curve_force.png"

b['FiberSim_batch']["batch_figures"]["ktr"].append(analysis)

# ktr-pCa curve

analysis["relative_to"] = "this_file"
analysis["results_folder"] = "sim_output"
analysis["data_field"] = "pCa"
analysis["output_data_file_string"] = "sim_output/analysis.xlsx"
analysis["output_image_file_string"] = "sim_output/ktr_curve_pCa.png"

b['FiberSim_batch']["batch_figures"]["ktr"].append(analysis)

# Save batch file

with open(job_file_string,'w') as f:
    json.dump(b, f, indent=4)
    



    

    
    


