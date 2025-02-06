import pytest
import pandas as pd
import os
import sys
from unittest.mock import patch, MagicMock

# Add the project directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_analysis import create_clean_data_folder, process_all_subjects_noisy_and_quiet, dataframe_by_trial_id

@pytest.fixture
def sample_dataframe():
    """יוצר DataFrame מדומה עבור ניסויים"""
    return pd.DataFrame({
        'trial_id': [1, 2, 3, 4],
        'trial_type': ['noisy', 'quiet', 'noisy', 'quiet'],
        'end timestamp [ns]': [2000000, 4000000, 6000000, 8000000],
        'start timestamp [ns]': [1000000, 3000000, 5000000, 7000000]
    })

def test_create_clean_data_folder():
    """בודק שהתיקייה Clean_data נוצרת אם היא לא קיימת"""
    with patch("os.path.exists", return_value=False), \
         patch("os.mkdir") as mock_mkdir:
        
        create_clean_data_folder()
        mock_mkdir.assert_called_once()  # מוודא שהתיקייה נוצרה

def test_process_all_subjects_noisy_and_quiet(sample_dataframe):
    """בודק שהפונקציה מחשבת נתונים נכונה"""
    with patch("os.listdir", return_value=["participant_1"]), \
         patch("os.path.isdir", return_value=True), \
         patch("pandas.read_csv", return_value=sample_dataframe), \
         patch("pandas.DataFrame.to_csv") as mock_to_csv:
        
        df = process_all_subjects_noisy_and_quiet()
        
        assert "noisy" in df.columns.levels[0]  # בודק שיש עמודות noisy
        assert "quiet" in df.columns.levels[0]  # בודק שיש עמודות quiet
        assert "fixations_on_face" in df.columns.levels[1]  # בודק שיש עמודות fixations
        
        mock_to_csv.assert_called_once()  # מוודא שהקובץ נוצר ונשמר

