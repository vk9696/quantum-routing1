import os
import pandas as pd
import matplotlib.pyplot as plt

# File paths
file_paths = [
    'data/cy_0.8_1_1.csv', 'data/cy_0.8_1_100.csv',
    'data/cy_0.7_1_1.csv', 'data/cy_0.7_1_100.csv',
    'data/cy_0.53_1_1.csv', 'data/cy_0.53_1_100.csv'
]

# Plotting
plt.figure(figsize=(10, 6))

# To manage special labeling
special_label_used = False

for file_path in file_paths:
    # Load data
    df = pd.read_csv(file_path)
    
    # Calculate ξ
    df['xi'] = df['HQ_percent'] / 100

    # Group by ξ and calculate average fidelity
    grouped_data = df.groupby('xi')['fidelity'].mean().reset_index()

    # Extracting threshold fidelity and approach type from file name
    parts = file_path.split('_')
    threshold_fidelity = float(parts[1])
    approach_index = parts[3].split('.')[0]
    approach_type = 'Shortest path' if approach_index == '1' else 'Efficiency aware'

    # Determine the label to use
    if threshold_fidelity == 0.8 and approach_type == 'Efficiency aware':
        label = 'Threshold fidelity = 0.8 (Both)'
        if not special_label_used:
            plt.plot(grouped_data['xi'], grouped_data['fidelity'], label=label)
            special_label_used = True
    elif threshold_fidelity == 0.8 and approach_type == 'Shortest path':
        continue 
    else:
        label = f"Threshold fidelity = {threshold_fidelity}, ({approach_type})"
        plt.plot(grouped_data['xi'], grouped_data['fidelity'], label=label)

# Set y-axis ticks
current_ticks = plt.yticks()[0]  # Get current ticks
new_ticks = sorted(set(current_ticks.tolist() + [0.5]))
plt.yticks(new_ticks)

plt.xlim(0.36, 1)
plt.xlabel('ξ')
plt.ylabel('Fidelity')
plt.title('Fidelity vs ξ')
plt.legend(loc='best', fontsize='x-small')
plt.grid(True)
plt.show()
