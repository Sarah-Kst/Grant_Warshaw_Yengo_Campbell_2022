# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 10:05:49 2021

@author: srhko
"""

import os, sys
import pandas as pd
import generate_protocols as gp

import json

# General path definitions

ROOT = os.path.dirname(__file__)
FIBERSIM_ROOT = os.path.join(ROOT, "..", "..", "..", "FiberSim")
FiberPy_ROOT = os.path.join(FIBERSIM_ROOT, "code","FiberPy","FiberPy")

sys.path.append(FiberPy_ROOT)

from package.modules.batch.batch import run_batch as rb

#### Run isometric activations

# Prepare batch file for isometric activations

# Variables
job_file_string = '../batch_multiple_isom_activations.json'

# Prepare batch file for isometric activations
b = dict()
b['FiberSim_batch'] = dict()
b['FiberSim_batch']["FiberCpp_exe"] = dict()
b['FiberSim_batch']["FiberCpp_exe"]["relative_to"] = "this_file"
b['FiberSim_batch']["FiberCpp_exe"]["exe_file"] = "../../FiberSim/bin/fibercpp.exe"

b['FiberSim_batch']["job"] = []

pCa_value = 4.5

model_list = ["model_poly", "model_load", "model_load_wall"]

for i, model_file in enumerate(model_list):

    job = gp.generate_isom_protocols(pCa_value, i+1)
    
    b['FiberSim_batch']["job"].append(job)
    
with open(job_file_string,'w') as f:
    json.dump(b, f, indent=4)

batch_file = "batch_multiple_isom_activations.json"

batch_file = os.path.join(ROOT, "..", batch_file)

rb(batch_file)

### Extract stationnary force, create loaded shortening 

#Prepare batch file for loaded shortenings 

job_file_string = '../batch_fv_and_power.json'

b = dict()
b['FiberSim_batch'] = dict()
b['FiberSim_batch']["FiberCpp_exe"] = dict()
b['FiberSim_batch']["FiberCpp_exe"]["relative_to"] = "this_file"
b['FiberSim_batch']["FiberCpp_exe"]["exe_file"] = "../../FiberSim/bin/fibercpp.exe"

b['FiberSim_batch']["job"] = []

b['FiberSim_batch']["batch_figures"] = dict()
b['FiberSim_batch']["batch_figures"]["force_velocity"] = []

job = []

  
for i, model_file in enumerate(model_list):
                
    pd_data = pd.read_csv(f'../sim_output/{i+1}/pCa_{10 * pCa_value:.0f}/pCa_{10 * pCa_value:.0f}_results.txt', delimiter = "\t")

    iso_force = pd_data["force"].iloc[-201:-1].mean()
    
    print(iso_force)

    job = gp.generate_load_protocols(iso_force, pCa_value, i+1, job)
        
b['FiberSim_batch']["job"] = job
                  

analysis = dict()

analysis["relative_to"] = "this_file"
analysis["results_folder"] = "sim_output"
analysis["fit_time_interval_s"] = [1.05,1.3]
analysis["output_data_file_string"] = "sim_output/analysis.xlsx"
analysis["output_image_file_string"] = "sim_output/fv_and_power.png"

b['FiberSim_batch']["batch_figures"]["force_velocity"].append(analysis)


with open(job_file_string,'w') as f:
    json.dump(b, f, indent=4)
    
## Run force-velocity curves

batch_file = "batch_fv_and_power.json"

batch_file = os.path.join(ROOT, "..", batch_file)

rb(batch_file)


    

    
    


