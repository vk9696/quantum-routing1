import pandas as pd
import matplotlib.pyplot as plt

# Total number of nodes in the network
total_nodes = 25

# Read all CSV filesS
data_0_8_1_1 = pd.read_csv('data/cy_0.8_1_1.csv')
data_0_8_1_100 = pd.read_csv('data/cy_0.8_1_100.csv')
data_0_7_1_1 = pd.read_csv('data/cy_0.7_1_1.csv')
data_0_7_1_100 = pd.read_csv('data/cy_0.7_1_100.csv')
data_0_5_1_1 = pd.read_csv('data/cy_0.53_1_1.csv')
data_0_5_1_100 = pd.read_csv('data/cy_0.53_1_100.csv')

# List of HQ_percent values to plot
hq_percent_values = [i for i in range(0, 101, 4)]

xi_values = []

# Lists to store blocking probabilities for different cases
blocking_probabilities_0_8_1_1 = []
blocking_probabilities_0_8_1_100 = []
blocking_probabilities_0_7_1_1 = []
blocking_probabilities_0_7_1_100 = []
blocking_probabilities_0_5_1_1 = [] 
blocking_probabilities_0_5_1_100 = [] 

for hq_percent in hq_percent_values:
    # Calculate HQ and LQ nodes
    hq_nodes = (hq_percent / 100.0) * total_nodes
    lq_nodes = total_nodes - hq_nodes
    
    # Calculate xi
    xi = hq_nodes / (lq_nodes + hq_nodes)
    xi_values.append(xi)
    
    filtered_df_0_7_1_1 = data_0_7_1_1[data_0_7_1_1['HQ_percent'] == hq_percent]
    filtered_df_0_7_1_100 = data_0_7_1_100[data_0_7_1_100['HQ_percent'] == hq_percent]
    filtered_df_0_5_1_1 = data_0_5_1_1[data_0_5_1_1['HQ_percent'] == hq_percent]
    filtered_df_0_5_1_100 = data_0_5_1_100[data_0_5_1_100['HQ_percent'] == hq_percent]
    filtered_df_0_8_1_1 = data_0_8_1_1[data_0_8_1_1['HQ_percent'] == hq_percent]
    filtered_df_0_8_1_100 = data_0_8_1_100[data_0_8_1_100['HQ_percent'] == hq_percent]

    filtered_df_0_7_1_1_clean = filtered_df_0_7_1_1[filtered_df_0_7_1_1['fidelity'] <= 1]
    filtered_df_0_7_1_100_clean = filtered_df_0_7_1_100[filtered_df_0_7_1_100['fidelity'] <= 1]
    filtered_df_0_5_1_1_clean = filtered_df_0_5_1_1[filtered_df_0_5_1_1['fidelity'] <= 1]
    filtered_df_0_5_1_100_clean = filtered_df_0_5_1_100[filtered_df_0_5_1_100['fidelity'] <= 1]
    filtered_df_0_8_1_1_clean = filtered_df_0_8_1_1[filtered_df_0_8_1_1['fidelity'] <= 1]
    filtered_df_0_8_1_100_clean = filtered_df_0_8_1_100[filtered_df_0_8_1_100['fidelity'] <= 1]

    blocking_prob_0_7_1_1 = (len(filtered_df_0_7_1_1) - len(filtered_df_0_7_1_1_clean)) / len(filtered_df_0_7_1_1)
    blocking_prob_0_7_1_100 = (len(filtered_df_0_7_1_100) - len(filtered_df_0_7_1_100_clean)) / len(filtered_df_0_7_1_100)
    blocking_prob_0_5_1_1 = (len(filtered_df_0_5_1_1) - len(filtered_df_0_5_1_1_clean)) / len(filtered_df_0_5_1_1)
    blocking_prob_0_5_1_100 = (len(filtered_df_0_5_1_100) - len(filtered_df_0_5_1_100_clean)) / len(filtered_df_0_5_1_100)
    blocking_prob_0_8_1_1 = (len(filtered_df_0_8_1_1) - len(filtered_df_0_8_1_1_clean)) / len(filtered_df_0_8_1_1)
    blocking_prob_0_8_1_100 = (len(filtered_df_0_8_1_100) - len(filtered_df_0_8_1_100_clean)) / len(filtered_df_0_8_1_100)

    blocking_probabilities_0_7_1_1.append(blocking_prob_0_7_1_1)
    blocking_probabilities_0_7_1_100.append(blocking_prob_0_7_1_100)
    blocking_probabilities_0_5_1_1.append(blocking_prob_0_5_1_1)
    blocking_probabilities_0_5_1_100.append(blocking_prob_0_5_1_100)
    blocking_probabilities_0_8_1_1.append(blocking_prob_0_8_1_1)
    blocking_probabilities_0_8_1_100.append(blocking_prob_0_8_1_100)

print(xi_values)
print(blocking_probabilities_0_7_1_1)
print(blocking_probabilities_0_5_1_1)
print(blocking_probabilities_0_8_1_1)
print(blocking_probabilities_0_7_1_100)
print(blocking_probabilities_0_5_1_100)
print(blocking_probabilities_0_8_1_100)

# Plotting
plt.plot(xi_values, blocking_probabilities_0_8_1_1)
plt.plot(xi_values, blocking_probabilities_0_8_1_100, label='Threshold fidelity = 0.8 (Both)')
plt.plot(xi_values, blocking_probabilities_0_7_1_1, label='Threshold fidelity = 0.7 (Shortest path)')
plt.plot(xi_values, blocking_probabilities_0_7_1_100, label='Threshold fidelity = 0.7 (Efficiency aware)')
plt.plot(xi_values, blocking_probabilities_0_5_1_1, label='Threshold fidelity = 0.53 (Shortest path)')
plt.plot(xi_values, blocking_probabilities_0_5_1_100, label='Threshold fidelity = 0.53 (Efficiency aware)')


plt.xlabel(r'$ \xi $')
plt.ylabel('$Blocking \ Probability$')
plt.title(rf'$Blocking \ Probability \ vs \ \xi$')
plt.legend()
plt.grid()
plt.show()
