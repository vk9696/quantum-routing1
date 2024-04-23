import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_new_ratio(hq_percent):
    return round(hq_percent / 100, 2)

fig, axs = plt.subplots(1, 1, figsize=(20, 10))

# Read the data and calculate the ratio
data_cy_0_8 = pd.read_csv('data/cylindrical_0.8.csv')
data_cy_0_8['new_ratio'] = calculate_new_ratio(data_cy_0_8['HQ_percent'])
data_cy_0_9 = pd.read_csv('data/cylindrical_0.9.csv')
data_cy_0_9['new_ratio'] = calculate_new_ratio(data_cy_0_9['HQ_percent'])
data_cy_0_99 = pd.read_csv('data/cylindrical_0.99.csv')
data_cy_0_99['new_ratio'] = calculate_new_ratio(data_cy_0_99['HQ_percent'])

ax2 = axs
marker_dict = {r'$\eta_l = 0.99$': 's', r'$\eta_l = 0.8$': '^'}  # square for 0.99 and triangle for 0.8

for data, label in zip([data_cy_0_99, data_cy_0_8], [r'$\eta_l = 0.99$', r'$\eta_l = 0.8$']):
    if not data.empty:
        avg_fidelity = data.groupby(['new_ratio', 'path_length'])['fidelity'].mean().reset_index()
        for length in avg_fidelity['path_length'].unique():
            if length == 7 or length == 11:
                length_data = avg_fidelity[avg_fidelity['path_length'] == length]
                ax2.plot(length_data['new_ratio'], length_data['fidelity'], label=f"{label}, Path Length = {length}", marker=marker_dict[label])
                
        ax2.set_xlabel(r'$\xi$')
        ax2.set_ylabel('$Fidelity$')
        ax2.legend(loc='lower right', fontsize='small')
        ax2.set_title(r'$\eta_h = 0.999$')

        ax2.set_ylim(0, 0.8 * 1.1)  # Adjust the multiplier for better visibility
        ax2.yaxis.set_major_locator(plt.MaxNLocator(7))  # Adjust the number of y-axis ticks as needed
        ax2.grid(True)




#plt.tight_layout(pad=6.0)
plt.show()
