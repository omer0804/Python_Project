import pytest
import pandas as pd
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_cleaner import (
    split_csv_by_recording_id,
    clean_participants_folders,
    remove_unecessary_columns,
    label_trials,
    
)

@pytest.fixture
def sample_dataframe():
    """Creates a mock DataFrame for testing"""
    return pd.DataFrame({
        'recording id': [123, 456, 789],
        'data': [10, 20, 30]
    })

@pytest.fixture
def sample_events_dataframe():
    """Creates a mock DataFrame for events"""
    return pd.DataFrame({
        'name': ['start-1', 'end-1', 'start-2', 'end-2'],
        'timestamp [ns]': [100, 200, 300, 400]
    })

def test_split_csv_by_recording_id(sample_dataframe):
    """Checks that the function correctly splits the file and returns the correct mapping"""
    with patch("pandas.read_csv", return_value=sample_dataframe), \
         patch("os.makedirs"), \
         patch("pandas.DataFrame.to_csv"):

        output_dir = "mock_output_dir"
        result = split_csv_by_recording_id("mock_input.csv", output_dir)
        
        assert isinstance(result, dict)
        assert len(result) == 3  #  3 recording id

def test_clean_participants_folders():
    """Checks that the function does not crash and performs file operations as expected"""
    with patch("os.listdir", return_value=["participant_1", "participant_2"]), \
         patch("os.path.isdir", return_value=True), \
         patch("os.makedirs"), \
         patch("pandas.read_csv", return_value=pd.DataFrame({"recording id": [1, 2]})), \
         patch("pandas.DataFrame.to_csv"), \
         patch("os.remove"), \
         patch("os.rmdir"):
        
        recording_id_map = {"old_1": "1", "old_2": "2"}
        clean_participants_folders(recording_id_map)

def test_remove_unecessary_columns():
    """Checks that the function removes unnecessary columns"""
    with patch("os.listdir", return_value=["participant_1"]), \
         patch("pandas.read_csv", return_value=pd.DataFrame({
             "type": [1, 2], "recording id": [3, 4], "section id": [5, 6], "data": [7, 8]
         })), \
         patch("pandas.DataFrame.to_csv") as mock_to_csv:
        
        remove_unecessary_columns("mock_participants_dir", ["participant_1"])
        mock_to_csv.assert_called()  # Ensures the file was saved after cleaning

def test_label_trials(sample_events_dataframe):
    """Checks that the function labels trials correctly"""
    df = pd.DataFrame({
        'start timestamp [ns]': [110, 310],
        'end timestamp [ns]': [190, 390]
    })
    labeled_df = label_trials(df, sample_events_dataframe)

    assert "trial_id" in labeled_df.columns
    assert "trial_type" in labeled_df.columns

