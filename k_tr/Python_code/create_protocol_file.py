import numpy as np
import pandas as pd
import os
import json

def create_protocol_file():
    """ Generates k_tr protocol files """

    step_n = 20;
    step_size = 50
    
    pCa_values = [4.5, 5.0, 5.5, 5.6, 5.7, 5.8]
    
    for i in range(0,(len(pCa_values))):
        # Make base_vectors vectors
        n_points = 15000
        time_step = 0.0001
    
        dt = time_step * np.ones(n_points)
        pCa = 9.0 * np.ones(n_points)
        dhsl = np.zeros(n_points)
        mode = -2 * np.ones(n_points)
    
        # Implement Ca ste
        pCa[250::] = pCa_values[i]
    
        # Implement step
        for j in range(5000, 5000+step_n):
            dhsl[j] = -step_size / step_n
            
        for j in range(5400, 5400 + step_n):
            dhsl[j] = step_size / step_n
        
        for j in range(4900, 5500):
            mode[j] = -1
    
        # Create pandas dataframe
        df = pd.DataFrame({'dt':dt, 'pCa':pCa, 'dhsl':dhsl, 'mode':mode})
        
        print(df)
        
        j = i +1
        
        # Write to file
        df.to_csv('../sim_input/1/protocol_%i.txt' % j, sep='\t', index=False)
        df.to_csv('../sim_input/2/protocol_%i.txt' % j, sep='\t', index=False)
        df.to_csv('../sim_input/3/protocol_%i.txt' % j, sep='\t', index=False)
        
        # Create output handler
        
        create_output_handler_file(1, j)
        create_output_handler_file(2, j)
        create_output_handler_file(3, j)
        
        
def create_output_handler_file(folder, val):
    # Writes an output handler file

    # Generate a file string
    
    file_string = os.path.join('sim_input', '%i' % folder,
                               ('output_handler_%i.json') % val )

    # Create the json struct
    ti = []
    
    ti_j = dict()
    ti_j['relative_to'] = 'this_file'
    ti_j['template_file_string'] = '../../template/template_summary.json'
    ti_j['output_file_string'] = os.path.join('../../sim_output', '%i' % folder,
                                              ('summary_%i.png') % val)
    ti.append(ti_j)

    t = dict()
    t['templated_images'] = ti

    # Write struct
    
    # Check the directory exists
    dir_name = os.path.dirname('../' + file_string)
    if (not os.path.isdir(dir_name)):
        os.makedirs(dir_name)

    with open('../' + file_string,'w') as f:
        json.dump(t, f, indent=4)

    
if __name__ == "__main__":
    create_protocol_file()
    
