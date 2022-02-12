## This repo allows to compare force-velocity and k_tr curves for three models with FiberSim:

1. Model with a polynomial detachment rate

2. Model with an exponential load-dependent rate

3. Model with an exponential load-dependent rate + wall for x > x_lim 

To obtain force-velocity curves:

1) Open "Python_code/run_tension_velocity.py"

2) Write the pCa value you want (line 40)

3) Run the Python script. This scripts starts with an isometric activation at the desired pCa. Then it calculates the isometric force F_iso to to generate loaded protocols for 0.1, 10, 20, 40, 80 and 100% of F_iso 

4) The force-velocity data for the 3 models (1 = poly, 2 = load-dep, 3 = load-dep + wall) are stored in sim_ouput/analysis.xlsx

5) You can run "Python_code/plot_fv.py" for a quick plot of the 3 force-velocity and force-power curves

To obtain k_tr curves:

1) Create_protocol_files allows to create a set of k_tr protocols for a serie of pCa values (line 12)

2) Create_batch_file allows to create an associated batch file (list of pCa values to be provided on line 28)

3) Once the batch file is created, call FiberPy to run it, like for a FiberSim demo, by typing "python FiberPy.py run_batch "../../../../Grant_Warshaw_Yengo_Campbell_2022\k_tr/batch_k_tr.json"

4) You can run "Python_code/plot_ktr.py" in Spyder for a quick superposed plot of the three k_tr curves


