# this code will help us plot graphs from the files we created in the data_analysis.py 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Use the Agg backend for matplotlib
import matplotlib
matplotlib.use('Agg')

# Load the data  
data_noisy_quiet = pd.read_csv(r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Clean_data\summary.csv', index_col=0, header=[0, 1, 2])
data_by_trials = pd.read_csv(r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Clean_data\trial_summary.csv', index_col=0, header=[0, 1, 2])

# Fixations on face: Noisy vs Quiet (Quantity and Duration)
def fixations_plot_noisy_vs_quiet(data):
    avg_row = data.loc['average']
    std_row = data.loc['std_dev']

    categories = ['noisy', 'quiet']
    quantity_means = [avg_row['noisy', 'fixations_on_face', 'quantity'], avg_row['quiet', 'fixations_on_face', 'quantity']]
    quantity_stds = [std_row['noisy', 'fixations_on_face', 'quantity'], std_row['quiet', 'fixations_on_face', 'quantity']]
    duration_means = [avg_row['noisy', 'fixations_on_face', 'duration'], avg_row['quiet', 'fixations_on_face', 'duration']]
    duration_stds = [std_row['noisy', 'fixations_on_face', 'duration'], std_row['quiet', 'fixations_on_face', 'duration']]

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Quantity
    axes[0].bar(categories, quantity_means, yerr=quantity_stds, capsize=5, color=['blue', 'orange'])
    axes[0].set_title('Fixations on Face Quantity: Noisy vs Quiet')
    axes[0].set_ylabel('Quantity')

    # Duration
    axes[1].bar(categories, duration_means, yerr=duration_stds, capsize=5, color=['blue', 'orange'])
    axes[1].set_title('Fixations on Face Duration: Noisy vs Quiet')
    axes[1].set_ylabel('Duration (s)')

    plt.tight_layout()
    plt.savefig(r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Clean_data\noisy_vs_quiet.png')

# Fixations on face per trial: Quantity and Duration
def plot_fixations_per_trial(data):
    trial_ids = sorted([int(float(col)) for col in data.columns.levels[0]])
    quantity_means = data.xs(('fixations_on_face', 'quantity'), axis=1, level=[1, 2]).loc['average']
    duration_means = data.xs(('fixations_on_face', 'duration'), axis=1, level=[1, 2]).loc['average']

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Quantity per trial
    axes[0].scatter(trial_ids, quantity_means, color='blue')
    m, b = np.polyfit(trial_ids, quantity_means, 1)
    axes[0].plot(trial_ids, m*np.array(trial_ids) + b, color='red')
    axes[0].set_title('Fixations on Face Quantity per Trial')
    axes[0].set_xlabel('Trial ID')
    axes[0].set_ylabel('Quantity')

    # Duration per trial
    axes[1].scatter(trial_ids, duration_means, color='blue')
    m, b = np.polyfit(trial_ids, duration_means, 1)
    axes[1].plot(trial_ids, m*np.array(trial_ids) + b, color='red')
    axes[1].set_title('Fixations on Face Duration per Trial')
    axes[1].set_xlabel('Trial ID')
    axes[1].set_ylabel('Duration (s)')

    plt.tight_layout()
    plt.savefig(r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Clean_data\fixations_per_trial.png')

# Blinks: Noisy vs Quiet (Quantity and Duration)
def blinks_plot_noisy_vs_quiet(data):
    avg_row = data.loc['average']
    std_row = data.loc['std_dev']

    categories = ['noisy', 'quiet']
    quantity_means = [avg_row['noisy', 'blinks', 'quantity'], avg_row['quiet', 'blinks', 'quantity']]
    quantity_stds = [std_row['noisy', 'blinks', 'quantity'], std_row['quiet', 'blinks', 'quantity']]
    duration_means = [avg_row['noisy', 'blinks', 'duration'], avg_row['quiet', 'blinks', 'duration']]
    duration_stds = [std_row['noisy', 'blinks', 'duration'], std_row['quiet', 'blinks', 'duration']]

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Quantity
    axes[0].bar(categories, quantity_means, yerr=quantity_stds, capsize=5, color=['blue', 'orange'])
    axes[0].set_title('Blinks Quantity: Noisy vs Quiet')
    axes[0].set_ylabel('Quantity')

    # Duration
    axes[1].bar(categories, duration_means, yerr=duration_stds, capsize=5, color=['blue', 'orange'])
    axes[1].set_title('Blinks Duration: Noisy vs Quiet')
    axes[1].set_ylabel('Duration (s)')

    plt.tight_layout()
    plt.savefig(r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Clean_data\blinks_noisy_vs_quiet.png')

# Blinks per trial: Quantity and Duration
def plot_blinks_per_trial(data):
    trial_ids = sorted([int(float(col)) for col in data.columns.levels[0]])
    quantity_means = data.xs(('blinks', 'quantity'), axis=1, level=[1, 2]).loc['average']
    duration_means = data.xs(('blinks', 'duration'), axis=1, level=[1, 2]).loc['average']

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Quantity per trial
    axes[0].scatter(trial_ids, quantity_means, color='blue')
    m, b = np.polyfit(trial_ids, quantity_means, 1)
    axes[0].plot(trial_ids, m*np.array(trial_ids) + b, color='red')
    axes[0].set_title('Blinks Quantity per Trial')
    axes[0].set_xlabel('Trial ID')
    axes[0].set_ylabel('Quantity')

    # Duration per trial
    axes[1].scatter(trial_ids, duration_means, color='blue')
    m, b = np.polyfit(trial_ids, duration_means, 1)
    axes[1].plot(trial_ids, m*np.array(trial_ids) + b, color='red')
    axes[1].set_title('Blinks Duration per Trial')
    axes[1].set_xlabel('Trial ID')
    axes[1].set_ylabel('Duration (s)')

    plt.tight_layout()
    plt.savefig(r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Clean_data\blinks_per_trial.png')

# Saccades: Noisy vs Quiet (Quantity and Duration)
def saccades_plot_noisy_vs_quiet(data):
    avg_row = data.loc['average']
    std_row = data.loc['std_dev']

    categories = ['noisy', 'quiet']
    quantity_means = [avg_row['noisy', 'saccades', 'quantity'], avg_row['quiet', 'saccades', 'quantity']]
    quantity_stds = [std_row['noisy', 'saccades', 'quantity'], std_row['quiet', 'saccades', 'quantity']]
    duration_means = [avg_row['noisy', 'saccades', 'duration'], avg_row['quiet', 'saccades', 'duration']]
    duration_stds = [std_row['noisy', 'saccades', 'duration'], std_row['quiet', 'saccades', 'duration']]

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Quantity
    axes[0].bar(categories, quantity_means, yerr=quantity_stds, capsize=5, color=['blue', 'orange'])
    axes[0].set_title('Saccades Quantity: Noisy vs Quiet')
    axes[0].set_ylabel('Quantity')

    # Duration
    axes[1].bar(categories, duration_means, yerr=duration_stds, capsize=5, color=['blue', 'orange'])
    axes[1].set_title('Saccades Duration: Noisy vs Quiet')
    axes[1].set_ylabel('Duration (s)')

    plt.tight_layout()
    plt.savefig(r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Clean_data\saccades_noisy_vs_quiet.png')

# Saccades per trial: Quantity and Duration
def plot_saccades_per_trial(data):
    trial_ids = sorted([int(float(col)) for col in data.columns.levels[0]])
    quantity_means = data.xs(('saccades', 'quantity'), axis=1, level=[1, 2]).loc['average']
    duration_means = data.xs(('saccades', 'duration'), axis=1, level=[1, 2]).loc['average']

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Quantity per trial
    axes[0].scatter(trial_ids, quantity_means, color='blue')
    m, b = np.polyfit(trial_ids, quantity_means, 1)
    axes[0].plot(trial_ids, m*np.array(trial_ids) + b, color='red')
    axes[0].set_title('Saccades Quantity per Trial')
    axes[0].set_xlabel('Trial ID')
    axes[0].set_ylabel('Quantity')

    # Duration per trial
    axes[1].scatter(trial_ids, duration_means, color='blue')
    m, b = np.polyfit(trial_ids, duration_means, 1)
    axes[1].plot(trial_ids, m*np.array(trial_ids) + b, color='red')
    axes[1].set_title('Saccades Duration per Trial')
    axes[1].set_xlabel('Trial ID')
    axes[1].set_ylabel('Duration (s)')

    plt.tight_layout()
    plt.savefig(r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Clean_data\saccades_per_trial.png')

# Plot the graphs
fixations_plot_noisy_vs_quiet(data_noisy_quiet)
plot_fixations_per_trial(data_by_trials)
blinks_plot_noisy_vs_quiet(data_noisy_quiet)
plot_blinks_per_trial(data_by_trials)
saccades_plot_noisy_vs_quiet(data_noisy_quiet)
plot_saccades_per_trial(data_by_trials)
