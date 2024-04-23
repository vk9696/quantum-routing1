import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read all three CSV files
data_1_1 = pd.read_csv('data/cy_0_1_1.csv')
data_1_100_new = pd.read_csv('data/cy_0_1_100.csv')

# List of HQ_percent values to plot
hq_percent_values = [20, 40]

# Adjust the figure size and create a figure for the subplots
fig, axes = plt.subplots(1, 2, figsize=(9, 3))  # Increased figure size
axes = axes.flatten()  # Flatten the axes array for easy indexing

for i, hq_percent in enumerate(hq_percent_values):
    # Filter the data for the specific HQ_percent value
    filtered_df_1_1 = data_1_1[data_1_1['HQ_percent'] == hq_percent]
    filtered_df_1_100_new = data_1_100_new[data_1_100_new['HQ_percent'] == hq_percent]

    # Adjust the path_order column
    filtered_df_1_1['path_order'] -= 0.25
    filtered_df_1_100_new['path_order'] += 0.25

    # Calculate average fidelities for each unique 'path_order'
    avg_fid_1_1 = filtered_df_1_1.groupby('path_order')['fidelity'].mean().reset_index()
    avg_fid_1_100_new = filtered_df_1_100_new.groupby('path_order')['fidelity'].mean().reset_index() 

    # Plot on the current subplot
    ax = axes[i]

    ax.scatter(filtered_df_1_1['path_order'] + np.random.randn(len(filtered_df_1_1)) * 0.05, filtered_df_1_1['fidelity'], s=0.05, label='$Individual \ Points \ (Shortest \ path)$')
    ax.scatter(filtered_df_1_100_new['path_order'] + np.random.randn(len(filtered_df_1_100_new)) * 0.05, filtered_df_1_100_new['fidelity'], s=0.05, label='$Individual \ Points \ (Efficiency \ aware)$')

    # Scatter plot for average fidelity
    ax.scatter(avg_fid_1_1['path_order'], avg_fid_1_1['fidelity'], color='blue', marker='x', s=40, label='$Average \ Fidelity \ (Shortest \ path)$')
    ax.scatter(avg_fid_1_100_new['path_order'], avg_fid_1_100_new['fidelity'], color='red', marker='x', s=40, label='$Average \ Fidelity \ (Efficiency \ aware)$')

    # Add text for average fidelity value
    textoffset = 0.02
    for index, row in avg_fid_1_1.iterrows():
        ax.text(row['path_order'], row['fidelity'] + textoffset, f'{row["fidelity"]:.3f}', ha='center', va='bottom', color='blue', fontsize=9, fontweight='bold')
    for index, row in avg_fid_1_100_new.iterrows():
        ax.text(row['path_order'], row['fidelity']+ textoffset, f'{row["fidelity"]:.3f}', ha='center', va='bottom', color='red', fontsize=9, fontweight='bold')
    
    # Add grid lines at specific x positions
    grid_positions = [1.5, 2.5, 3.5, 4.5]
    for pos in grid_positions:
        ax.axvline(x=pos, color='gray', linestyle='--', linewidth=0.5)

    titles = ["a)", "b)"] 
    ax.set_xlabel(r'$\theta$')
    ax.set_ylabel('$Fidelity$')
    ax.set_title(fr'{titles[i]} $\xi$ = {hq_percent / 100:.1f}')
    ax.set_ylim(0.2, 0.9)
    
    legend = ax.legend(fontsize='x-small', scatterpoints=1)
    for handle in legend.legendHandles:
        handle.set_sizes([30.0])

# Adjust the layout
plt.subplots_adjust(wspace=0, hspace=0)  # Adjust the spacing

plt.tight_layout()
plt.show()
