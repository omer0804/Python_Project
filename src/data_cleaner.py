import pandas as pd
import os


def split_csv_by_recording_id(input_file, output_dir):
    """
    Split a CSV file of fixations on face by 'recording id' (per participant) column and save each recording id to a separate CSV file.
    Also, create a dictionary mapping original recording ids to new sequential numbers.(for my comfort)
    """
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Get unique recording ids
    recording_ids = df['recording id'].unique() #rn only 5, 60 in future
    
    # Create a dictionary to map original recording ids to new sequential numbers
    recording_id_map = {recording_id: str(idx + 1) for idx, recording_id in enumerate(recording_ids)} # +1 to start from 1
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True) #participants dir
    
    # Split the dataframe by recording id and save to separate CSV files
    for recording_id in recording_ids:
        df_recording = df[df['recording id'] == recording_id].copy()
        new_recording_id = recording_id_map[recording_id]
        df_recording.loc[:, 'recording id'] = new_recording_id
        participant_folder = os.path.join(output_dir, new_recording_id)
        os.makedirs(participant_folder, exist_ok=True)
        output_file = os.path.join(participant_folder, "fixations_on_face.csv")
        df_recording.to_csv(output_file, index=False)
    
    return recording_id_map 

# running the function
input_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'Raw_Data', 'fixations_on_face.csv')
output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'Raw_Data', 'participants')
recording_id_map = split_csv_by_recording_id(input_file, output_dir)

def clean_participants_folders(recording_id_map):
    """
    Clean up the participants folders by renaming them to a sequential number and keeping only specific files (blinks, events, saccades).
    Also update the 'recording id' column in the files to match the new folder names.
    """
    participants_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'Raw_Data', 'participants')
    
    # Get list of participant folders and sort them
    participant_folders = sorted(os.listdir(participants_dir))
    
    # Combine files into the folder {new_recording_id}
    for folder in participant_folders:
        old_folder_path = os.path.join(participants_dir, folder)
        matching_recording_id = next((rid for rid in recording_id_map if rid[:8] in folder), None)
        if matching_recording_id:
            new_folder_name = recording_id_map[matching_recording_id]
            new_folder_path = os.path.join(participants_dir, new_folder_name)
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
            
            # Move files to the new folder and update 'recording id' column
            for file_name in os.listdir(old_folder_path):
                if file_name in ['blinks.csv', 'events.csv', 'saccades.csv', 'fixations_on_face.csv']:
                    old_file_path = os.path.join(old_folder_path, file_name)
                    new_file_path = os.path.join(new_folder_path, file_name)
                    df = pd.read_csv(old_file_path)
                    df['recording id'] = new_folder_name
                    df.to_csv(new_file_path, index=False)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                else:
                    file_path = os.path.join(old_folder_path, file_name)
                    if os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                        except PermissionError:
                            print(f"Could not delete {file_path} because it is open.")
            os.rmdir(old_folder_path)

# running the function
clean_participants_folders(recording_id_map)

def remove_unecessary_columns(participants_dir, participant_folders):
    """  
    Remove 'type', 'recording id', 'section id' columns from all files in the participant folders.
    """ 
    for folder in participant_folders:
        folder_path = os.path.join(participants_dir, folder)
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            # check if the file has 'type', 'recording id', 'section id' columns and delete them
            df = pd.read_csv(file_path)
            if 'type' in df.columns:
                df.drop(columns=['type'], inplace=True)
            if 'recording id' in df.columns:
                df.drop(columns=['recording id'], inplace=True)
            if 'section id' in df.columns:
                df.drop(columns=['section id'], inplace=True)
            df.to_csv(file_path, index=False)

# running the function
participants_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'Raw_Data', 'participants')
participant_folders = sorted(os.listdir(participants_dir))
remove_unecessary_columns(participants_dir, participant_folders)

def label_trials(df, events):
    df['trial_id'] = None
    df['trial_type'] = None

    for _, event in events.iterrows():
        if '-' in event['name']:
            trial_type = "quiet" if "start" in event['name'] and "dist" not in event['name'] else "noisy"
            trial_id = int(event['name'].split('-')[1])
            start_time = event['timestamp [ns]']

            # Identify the corresponding end time
            end_event_name = f"end-{trial_id}"
            end_time_series = events[events['name'] == end_event_name]['timestamp [ns]']
            if not end_time_series.empty:
                end_time = end_time_series.iloc[0]
            else:
                continue

            # Label rows within the time range
            mask = (df['start timestamp [ns]'] >= start_time) & (df['start timestamp [ns]'] <= end_time)
            if mask.any():
                df.loc[mask, 'trial_id'] = trial_id
                df.loc[mask, 'trial_type'] = trial_type

    return df


for folder in participant_folders:
    folder_path = os.path.join(participants_dir, folder)
    events_file = os.path.join(folder_path, 'events.csv')
    events_df = pd.read_csv(events_file)
    for file_name in os.listdir(folder_path):
        if file_name in ['fixations_on_face.csv', 'blinks.csv', 'saccades.csv']:
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df = label_trials(df, events_df)
            df.to_csv(file_path, index=False)

def delete_data_not_in_trials(participants_dir, participant_folders):
    """
    Delete rows in the fixations_on_face.csv, blinks.csv, and saccades.csv files that are not part of a trial.
    """
    for folder in participant_folders:
        folder_path = os.path.join(participants_dir, folder)
        events_file = os.path.join(folder_path, 'events.csv')
        events_df = pd.read_csv(events_file)
        for file_name in os.listdir(folder_path):
            if file_name in ['fixations_on_face.csv', 'blinks.csv', 'saccades.csv']:
                file_path = os.path.join(folder_path, file_name)
                df = pd.read_csv(file_path)
                trial_ids = events_df['name'].apply(lambda x: x.split('-')[1] if '-' in x else None).dropna().astype(int)
                df = df[df['trial_id'].isin(trial_ids)]
                df.to_csv(file_path, index=False)
    
# running delete_data_not_in_trials
participants_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'Raw_Data', 'participants')
participant_folders = sorted(os.listdir(participants_dir))
delete_data_not_in_trials(participants_dir, participant_folders)
