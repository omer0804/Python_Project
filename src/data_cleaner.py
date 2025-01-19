import pandas as pd
import os

def split_csv_by_recording_id(input_file, output_dir):
    """
    Split a CSV file of fixations on face by 'recording id' (per participant) column and save each subset to a separate CSV file.
    Also, create a dictionary mapping original recording ids to new sequential numbers.
    """
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Get unique recording ids
    recording_ids = df['recording id'].unique()
    
    # Create a dictionary to map original recording ids to new sequential numbers
    recording_id_map = {recording_id: str(idx + 1) for idx, recording_id in enumerate(recording_ids)}
    
    # Print the dictionary for debugging
    print("Recording ID Map:", recording_id_map)
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Split the dataframe by recording id and save to separate CSV files
    for recording_id in recording_ids:
        df_recording = df[df['recording id'] == recording_id].copy()
        new_recording_id = recording_id_map[recording_id]
        df_recording.loc[:, 'recording id'] = new_recording_id
        output_file = os.path.join(output_dir, f"{new_recording_id}.csv")
        df_recording.to_csv(output_file, index=False)
    
    return recording_id_map

# running the function
input_file = r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Raw_Data\fixations_on_face.csv'
output_dir = r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Raw_Data\fixations_on_face_by_recording'
recording_id_map = split_csv_by_recording_id(input_file, output_dir)

def clean_participants_folders(recording_id_map):
    """
    Clean up the participants folders by renaming them to a sequential number and keeping only specific files (blinks, events, saccades).
    Also update the 'recording id' column in the files to match the new folder names.
    Also match the 'recording id' in the fixations_on_face_by_recording files to the new folder names by the recording id.
    """
    participants_dir = r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Raw_Data\participants'
    fixations_dir = r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Raw_Data\fixations_on_face_by_recording'
    
    # Get list of participant folders and sort them
    participant_folders = sorted(os.listdir(participants_dir))
    
    # Rename participant folders to sequential numbers based on the recording_id_map
    for folder in participant_folders:
        old_folder_path = os.path.join(participants_dir, folder)
        # Check if the folder name contains the first 8 characters of any recording id
        matching_recording_id = next((rid for rid in recording_id_map if rid[:8] in folder), None)
        if matching_recording_id:
            new_folder_name = recording_id_map[matching_recording_id]
            new_folder_path = os.path.join(participants_dir, new_folder_name)
            os.rename(old_folder_path, new_folder_path)
            
            # Keep only specific files and update 'recording id' column
            for file_name in os.listdir(new_folder_path):
                if file_name in ['blinks.csv', 'events.csv', 'saccades.csv']:
                    file_path = os.path.join(new_folder_path, file_name)
                    df = pd.read_csv(file_path)
                    df['recording id'] = new_folder_name
                    df.to_csv(file_path, index=False)
                else:
                    os.remove(os.path.join(new_folder_path, file_name))
    
    # Update 'recording id' in fixations_on_face_by_recording files and rename files
    for file_name in os.listdir(fixations_dir):
        old_file_path = os.path.join(fixations_dir, file_name)
        original_recording_id = file_name.split('.')[0]
        if original_recording_id in recording_id_map:
            new_file_name = recording_id_map[original_recording_id] + '.csv'
            new_file_path = os.path.join(fixations_dir, new_file_name)
            
            df = pd.read_csv(old_file_path)
            df['recording id'] = new_file_name.split('.')[0]
            df.to_csv(new_file_path, index=False)
            
            os.remove(old_file_path)

# running the function
clean_participants_folders(recording_id_map)