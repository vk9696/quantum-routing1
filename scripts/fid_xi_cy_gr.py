import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_new_ratio(hq_percent):
    return round(hq_percent / 100, 2)

# Initialize the 2x2 subplots
fig, axs = plt.subplots(2, 2, figsize=(20, 10))

# Read and prepare data for first subplot (a)
data_gr_0_8 = pd.read_csv('data/grid_0.8.csv')
data_gr_0_8['new_ratio'] = calculate_new_ratio(data_gr_0_8['HQ_percent'])

# First subplot (a)
ax1 = axs[0, 0]
if not data_gr_0_8.empty:
    avg_fidelity = data_gr_0_8.groupby(['new_ratio', 'path_length'])['fidelity'].mean().reset_index()
    for length in avg_fidelity['path_length'].unique():
         if length != 0:
            length_data = avg_fidelity[avg_fidelity['path_length'] == length]
            ax1.plot(length_data['new_ratio'], length_data['fidelity'], label=f'Path Length {length}')
    ax1.set_xlabel(r'$\xi$')
    ax1.set_ylabel('$Fidelity$')
    ax1.legend(loc='best', fontsize='x-small')
    ax1.set_title('(a) Grid network  $(\eta_h = 0.999$, $\eta_l = 0.8)$')

    ax1.set_ylim(0, max(data_gr_0_8['fidelity']) * 1.1)
    ax1.yaxis.set_major_locator(plt.MaxNLocator(5)) 
    ax1.grid()


# Third subplot (b)
ax3 = axs[0, 1]
if not data_gr_0_8[['fidelity', 'new_ratio']].dropna().empty:
    sns.boxplot(x='new_ratio', y='fidelity', data=data_gr_0_8[['fidelity', 'new_ratio']], ax=ax3)
    ax3.set_xlabel(r'$\xi$')
    ax3.set_ylabel('$Fidelity$')
    ax3.set_title('(b) Grid network  $(\eta_h = 0.999$, $\eta_l = 0.8)$')

    # Adjust the x-axis tick rotation angle and spacing
    ax3.tick_params(axis='x', rotation=0)
    ax3.xaxis.set_major_locator(plt.MaxNLocator(12))

    ax3.set_ylim(0, max(data_gr_0_8['fidelity']) * 1.1) 
    ax3.yaxis.set_major_locator(plt.MaxNLocator(5)) 
    ax3.grid()


    # Remove the face color of the boxes
    for patch in ax3.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

# Read and prepare data for second subplot (c)
data_cy_0_8 = pd.read_csv('data/cylindrical_0.8.csv')
data_cy_0_8['new_ratio'] = calculate_new_ratio(data_cy_0_8['HQ_percent'])

# Second subplot (c)
ax2 = axs[1, 0]
if not data_cy_0_8.empty:
    avg_fidelity = data_cy_0_8.groupby(['new_ratio', 'path_length'])['fidelity'].mean().reset_index()
    for length in avg_fidelity['path_length'].unique():
        length_data = avg_fidelity[avg_fidelity['path_length'] == length]
        ax2.plot(length_data['new_ratio'], length_data['fidelity'], label=f'Path Length {length}')
    ax2.set_xlabel(r'$\xi$')
    ax2.set_ylabel('$Fidelity$')
    ax2.legend(loc='best', fontsize='x-small')
    ax2.set_title('(c) Cylindrical network  $(\eta_h = 0.999$, $\eta_l = 0.8)$')

    ax2.set_ylim(0, max(data_cy_0_8['fidelity']) * 1.1)
    ax2.yaxis.set_major_locator(plt.MaxNLocator(5)) 
    ax2.grid()

# Fourth subplot (d)
ax4 = axs[1, 1]
if not data_cy_0_8[['fidelity', 'new_ratio']].dropna().empty:
    sns.boxplot(x='new_ratio', y='fidelity', data=data_cy_0_8[['fidelity', 'new_ratio']], ax=ax4)
    ax4.set_xlabel(r'$\xi$')
    ax4.set_ylabel('$Fidelity$')
    ax4.set_title('(d) Cylindrical network  $(\eta_h = 0.999$, $\eta_l = 0.8)$')

    # Adjust the x-axis tick rotation angle and spacing
    ax4.tick_params(axis='x', rotation=0)
    ax4.xaxis.set_major_locator(plt.MaxNLocator(12))

    ax4.set_ylim(0, max(data_cy_0_8['fidelity']) * 1.1)
    ax4.yaxis.set_major_locator(plt.MaxNLocator(5))
    ax4.grid()

    # Remove the face color of the boxes
    for patch in ax4.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

plt.tight_layout(pad=6.0)
plt.show()