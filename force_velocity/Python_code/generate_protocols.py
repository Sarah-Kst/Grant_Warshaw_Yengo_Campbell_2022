# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 14:47:07 2021

@author: kscamp3
"""

import os
import json

import numpy as np
import pandas as pd


def generate_isom_protocols(pCa_val, curve):
    """ Create isometric protocol for a given pCa value and model file (curve) """


    prot = dict()
    prot['dt'] = 0.0001
    prot['n_points'] = 10000
    prot['initial_pCa'] = 9.0
    prot['n_step_pCa'] = 500
    prot['step_pCa'] = pCa_val
    prot['n_release'] = 10000
   
    # Loop through relative force values

    prot_file_string = write_isom_protocol(prot, curve)
    output_handler_file_string = write_output_handler_isom(prot, curve)

    # Add in a job
    j=dict()
    j['relative_to'] = 'this_file'
    j['model_file'] = os.path.join('sim_input', '%i' % curve,'model.json')
    j['options_file'] = 'sim_input/sim_options.json'
    j['protocol_file'] = prot_file_string
    j['results_file'] = os.path.join('sim_output', '%i' % curve,
                                      ('pCa_%.0f' % (10 * prot['step_pCa'])),
                                      ('pCa_%.0f_results.txt' % (10 * prot['step_pCa'])))
                                     
    j['output_handler_file'] = output_handler_file_string
        
    return j


def generate_load_protocols(iso_force, pCa, model, job):
    """ Create loaded shortening protocols """    

    rel_f = [0.001,0.1,0.2,0.4,0.8,1]

    prot = dict()
    prot['dt'] = 0.0001
    prot['n_points'] = 15000
    prot['initial_pCa'] = 9.0
    prot['n_step_pCa'] = 500
    prot['step_pCa'] = pCa
    prot['n_release'] = 10000
    prot['iso_force'] = iso_force

    
    # Loop through relative force values
    for r in rel_f:
        prot['curve'] = model
        prot['rel_f'] = r
        prot_file_string = write_loaded_protocol(prot)
        output_handler_file_string = write_output_handler_load(prot)

        # Add in a job
        j=dict()
        j['relative_to'] = 'this_file'
        j['model_file'] = os.path.join('sim_input', '%i' % model, 'model.json')
        j['options_file'] = 'sim_input/sim_options.json'
        j['protocol_file'] = prot_file_string
        j['results_file'] = os.path.join('sim_output',
                                          ('%.0f' % prot['curve']),
                                          ('results_%.0f.txt' % (100 * prot['rel_f'])))
                                         
        j['output_handler_file'] = output_handler_file_string

        job.append(j)
        
        print(prot_file_string)

    return job


def write_isom_protocol(prot, curve):
    # Write a protocol

    # Generate a file string
    file_string = os.path.join('sim_input', '%i' % curve,
                               ('pCa_%.0f' % (10 * prot['step_pCa'])),
                               ('pCa_%.0f.txt' % (10 * prot['step_pCa'])))

    # Now generate a protocol
    dt = prot['dt'] * np.ones(prot['n_points'])
    pCa = prot['initial_pCa'] * np.ones(prot['n_points'])
    pCa[prot['n_step_pCa']::] = prot['step_pCa']
    dhsl = np.zeros(prot['n_points'])
    mode = -2 * np.ones(prot['n_points'])

    d = {'dt': dt, 'pCa': pCa, 'dhsl': dhsl, 'mode': mode}
    df = pd.DataFrame(data=d)

    # Check the directory exists
    dir_name = os.path.dirname('../' + file_string)
    if (not os.path.isdir(dir_name)):
        os.makedirs(dir_name)

    # Write protocol
    df.to_csv('../' + file_string, sep='\t', index=False)
    
    # Return
    return file_string

def write_loaded_protocol(prot):
    # Write a protocol

    # Generate a file string
    file_string = os.path.join('sim_input', '%i' % prot['curve'],
                               ('rel_f_%.0f' % (100 * prot['rel_f'])),
                               ('prot_rel_f_%.0f.txt' % (100 * prot['rel_f'])))

    # Now generate a protocol
    dt = prot['dt'] * np.ones(prot['n_points'])
    pCa = prot['initial_pCa'] * np.ones(prot['n_points'])
    pCa[prot['n_step_pCa']::] = prot['step_pCa']
    dhsl = np.zeros(prot['n_points'])
    mode = -2 * np.ones(prot['n_points'])
    mode[prot['n_release']::] = prot['rel_f'] * prot['iso_force']

    d = {'dt': dt, 'pCa': pCa, 'dhsl': dhsl, 'mode': mode}
    df = pd.DataFrame(data=d)

    # Check the directory exists
    dir_name = os.path.dirname('../' + file_string)
    if (not os.path.isdir(dir_name)):
        os.makedirs(dir_name)

    # Write protocol
    df.to_csv('../' + file_string, sep='\t', index=False)
    
    # Return
    return file_string


def write_output_handler_load(prot):
    # Writes an output handler file

    # Generate a file string
    file_string = os.path.join('sim_input',
                               ('%i' % prot['curve']),
                               ('rel_f_%.0f' % (100 * prot['rel_f'])),
                               ('output_handler_%.0f.json') %
                                   (100 * prot['rel_f']))

    # Create the json struct
    ti = []
    ti_j = dict()
    ti_j['relative_to'] = 'this_file'
    ti_j['template_file_string'] = '../../../template/template_summary.json'
    ti_j['output_file_string'] = os.path.join('../../../sim_output',
                                              ('%i' % prot['curve']),
                                              ('summary_%.0f.png') % (100 * prot['rel_f']))
    ti.append(ti_j)

    t = dict()
    t['templated_images'] = ti
    
    print(t)

    # Write struct
    
    # Check the directory exists
    dir_name = os.path.dirname('../' + file_string)
    if (not os.path.isdir(dir_name)):
        os.makedirs(dir_name)

    with open('../' + file_string,'w') as f:
        json.dump(t, f, indent=4)

    print(file_string)

    # Return
    return file_string

def write_output_handler_isom(prot, curve):
    # Writes an output handler file

    # Generate a file string
    
    file_string = os.path.join('sim_input', str(curve),
                               ('pCa_%.0f' % (10 * prot['step_pCa'])),
                               ('output_handler_%.0f.json') %
                                   (10 * prot['step_pCa']))

    # Create the json struct
    ti = []
    ti_j = dict()
    ti_j['relative_to'] = 'this_file'
    ti_j['template_file_string'] = '../../../template/template_summary.json'
    ti_j['output_file_string'] = os.path.join('../../../sim_output', str(curve),
                                              ('pCa_%.0f' % (10 * prot['step_pCa'])),
                                              ('summary_isom_%.0f.png') % (10 * prot['step_pCa']))
    ti.append(ti_j)

    t = dict()
    t['templated_images'] = ti
    
    print(t)

    # Write struct
    
    # Check the directory exists
    dir_name = os.path.dirname('../' + file_string)
    if (not os.path.isdir(dir_name)):
        os.makedirs(dir_name)

    with open('../' + file_string,'w') as f:
        json.dump(t, f, indent=4)

    print(file_string)

    # Return
    return file_string