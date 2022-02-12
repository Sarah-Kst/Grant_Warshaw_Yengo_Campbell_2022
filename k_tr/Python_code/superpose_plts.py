import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


plt.rcParams.update({'font.family': "Arial"})
plt.rcParams.update({'font.size': 14}) 

color_set = ["#4110d9", "#9500ba", "#be0098", "#d50076", "#e00056", "#e2003a", "#dc1b20"]

    
def analyze_simulations():

    results_file_string_base = '../sim_output/2/results_'

    # Make a figure
    fig = plt.figure(constrained_layout=True)
    fig.set_size_inches([6, 6])
    spec = gridspec.GridSpec(nrows=3, ncols=1, figure=fig,
                             wspace=1)
    axs=[]
    for r in range(0,3):
        for c in range(0,1):
            axs.append(fig.add_subplot(spec[r,c]))
            
    for i in range(3):
    
        axs[i].spines['top'].set_visible(False)
        axs[i].spines['right'].set_visible(False)
        axs[i].set_xlim([0,2.5])
        axs[i].set_xticks([0,2.5])
    
        for axis in ['top','bottom','left','right']:
            axs[i].spines[axis].set_linewidth(1.5)
        
        for tick in axs[i].yaxis.get_major_ticks():
            tick.label.set_fontsize(14) 
        
        axs[i].tick_params(direction = "out", length = 6, width = 1.5)

    axs[0].spines['bottom'].set_visible(True)


    for i in range(0,2):
        rfs = ('%s%i.txt' % (results_file_string_base, i+1))

        d = pd.read_csv(rfs, sep='\t')

        x = d['time']

        axs[0].plot(x, d['pCa'], color = color_set[i])
        axs[0].set_ylim([9.5, 4])
        axs[0].set_ylabel('pCa', rotation=0, labelpad = 30)

        axs[1].plot(x, d['hs_length'], color = color_set[i])
        axs[1].set_ylim([1040, 1110])
        axs[1].set_ylabel('HS length \n(nm)', rotation=0, labelpad = 30)
        
        axs[2].plot(x, d['force']/1000, color = color_set[i])
        axs[2].set_ylim([0, 250])
        axs[2].set_ylabel("Force \n (kN m$^{\\mathregular{-2}}$)", rotation=0, labelpad = 35)
        axs[2].set_xlabel("Time (s)")
        

if __name__ == "__main__":
    analyze_simulations()
