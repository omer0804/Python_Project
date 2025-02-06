import pytest
import pandas as pd
import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_visualizer import plot_metric_noisy_vs_quiet, plot_metric_per_trial


BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'Clean_data')
SUMMARY_FILE = os.path.join(BASE_PATH, 'summary.csv')
TRIAL_FILE = os.path.join(BASE_PATH, 'trial_summary.csv')

@pytest.fixture
def summary_data():
    """Loads the summary.csv file for testing"""
    return pd.read_csv(SUMMARY_FILE, index_col=0, header=[0, 1, 2])

@pytest.fixture
def trial_data():
    """Loads the trial_summary.csv file for testing"""
    return pd.read_csv(TRIAL_FILE, index_col=0, header=[0, 1, 2])

def test_plot_metric_noisy_vs_quiet(summary_data):
    """Checks that graphs are successfully created for Noisy vs Quiet data"""
    with patch("matplotlib.pyplot.savefig") as mock_savefig:
        plot_metric_noisy_vs_quiet(summary_data, 'fixations_on_face', 'Fixations on Face', 'fixations')
        plot_metric_noisy_vs_quiet(summary_data, 'blinks', 'Blinks', 'blinks')
        plot_metric_noisy_vs_quiet(summary_data, 'saccades', 'Saccades', 'saccades')
        
        # Ensures the graphs were saved
        assert mock_savefig.call_count == 3, "Three graphs should have been saved"
        for call in mock_savefig.call_args_list:
            filename = call[0][0]
            assert filename.startswith(os.path.join(BASE_PATH, "fixations")) or \
                   filename.startswith(os.path.join(BASE_PATH, "blinks")) or \
                   filename.startswith(os.path.join(BASE_PATH, "saccades"))

def test_plot_metric_per_trial(trial_data):
    """Checks that graphs are successfully created by Trial ID"""
    with patch("matplotlib.pyplot.savefig") as mock_savefig:
        plot_metric_per_trial(trial_data, 'fixations_on_face', 'Fixations on Face', 'fixations')
        plot_metric_per_trial(trial_data, 'blinks', 'Blinks', 'blinks')
        plot_metric_per_trial(trial_data, 'saccades', 'Saccades', 'saccades')

        
        assert mock_savefig.call_count == 3, "Three graphs should have been saved"
        for call in mock_savefig.call_args_list:
            filename = call[0][0]
            assert filename.startswith(os.path.join(BASE_PATH, "fixations")) or \
                   filename.startswith(os.path.join(BASE_PATH, "blinks")) or \
                   filename.startswith(os.path.join(BASE_PATH, "saccades"))
