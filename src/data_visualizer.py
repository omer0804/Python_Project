# this code will help us plot graphs from the files we created in the data_analysis.py 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Use the Agg backend for matplotlib
import matplotlib
matplotlib.use('Agg')

# Base path for saving plots
BASE_PATH = r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Clean_data'

# Load the data  
data_noisy_quiet = pd.read_csv(f'{BASE_PATH}/summary.csv', index_col=0, header=[0, 1, 2])
data_by_trials = pd.read_csv(f'{BASE_PATH}/trial_summary.csv', index_col=0, header=[0, 1, 2])

# Data validation
if 'average' not in data_noisy_quiet.index or 'std_dev' not in data_noisy_quiet.index:
    raise ValueError("The required rows ('average', 'std_dev') are missing from the data.")

# General-purpose function for plotting noisy vs quiet data
def plot_metric_noisy_vs_quiet(data, metric, title_prefix, filename_prefix):
    avg_row = data.loc['average']
    std_row = data.loc['std_dev']

    categories = ['noisy', 'quiet']
    quantity_means = [avg_row['noisy', metric, 'quantity'], avg_row['quiet', metric, 'quantity']]
    quantity_stds = [std_row['noisy', metric, 'quantity'], std_row['quiet', metric, 'quantity']]
    duration_means = [avg_row['noisy', metric, 'duration'], avg_row['quiet', metric, 'duration']]
    duration_stds = [std_row['noisy', metric, 'duration'], std_row['quiet', metric, 'duration']]

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].bar(categories, quantity_means, yerr=quantity_stds, capsize=5, color=['blue', 'orange'])
    axes[0].set_title(f'{title_prefix} Quantity: Noisy vs Quiet')
    axes[0].set_ylabel('Quantity')

    axes[1].bar(categories, duration_means, yerr=duration_stds, capsize=5, color=['blue', 'orange'])
    axes[1].set_title(f'{title_prefix} Duration: Noisy vs Quiet')
    axes[1].set_ylabel('Duration (s)')

    plt.tight_layout()
    plt.savefig(f'{BASE_PATH}/{filename_prefix}_noisy_vs_quiet.png')

# Plotting functions for different metrics
plot_metric_noisy_vs_quiet(data_noisy_quiet, 'fixations_on_face', 'Fixations on Face', 'fixations')
plot_metric_noisy_vs_quiet(data_noisy_quiet, 'blinks', 'Blinks', 'blinks')
plot_metric_noisy_vs_quiet(data_noisy_quiet, 'saccades', 'Saccades', 'saccades')

# Function for plotting per trial data
def plot_metric_per_trial(data, metric, title_prefix, filename_prefix):
    try:
        trial_ids = sorted([int(float(col)) for col in data.columns.levels[0]])
    except ValueError as e:
        raise ValueError("Trial IDs must be numeric values.") from e

    quantity_means = data.xs((metric, 'quantity'), axis=1, level=[1, 2]).loc['average']
    duration_means = data.xs((metric, 'duration'), axis=1, level=[1, 2]).loc['average']

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Quantity per trial
    axes[0].scatter(trial_ids, quantity_means, color='blue')
    m, b = np.polyfit(trial_ids, quantity_means, 1)
    axes[0].plot(trial_ids, m*np.array(trial_ids) + b, color='red')
    axes[0].set_title(f'{title_prefix} Quantity per Trial')
    axes[0].set_xlabel('Trial ID')
    axes[0].set_ylabel('Quantity')

    # Duration per trial
    axes[1].scatter(trial_ids, duration_means, color='blue')
    m, b = np.polyfit(trial_ids, duration_means, 1)
    axes[1].plot(trial_ids, m*np.array(trial_ids) + b, color='red')
    axes[1].set_title(f'{title_prefix} Duration per Trial')
    axes[1].set_xlabel('Trial ID')
    axes[1].set_ylabel('Duration (s)')

    plt.tight_layout()
    plt.savefig(f'{BASE_PATH}/{filename_prefix}_per_trial.png')

# Plotting functions for different metrics per trial
plot_metric_per_trial(data_by_trials, 'fixations_on_face', 'Fixations on Face', 'fixations')
plot_metric_per_trial(data_by_trials, 'blinks', 'Blinks', 'blinks')
plot_metric_per_trial(data_by_trials, 'saccades', 'Saccades', 'saccades')
