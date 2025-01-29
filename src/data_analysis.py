import os
import pandas as pd

# Calculate the average for each experimenter and each variable
def create_clean_data_folder():
    r"""create a folder for Clean_data in C:\Users\USER\Desktop\Advanced Python Course\Python Project\data
    skip it if it already exists
    """
    clean_data_folder = r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Clean_data'
    if not os.path.exists(clean_data_folder):
        os.mkdir(clean_data_folder)
    else:
        print('Clean_data folder already exists.')
    
# running the function
create_clean_data_folder()

def process_all_subjects_noisy_and_quiet():
    base_path = r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Raw_Data\participants'
    columns = pd.MultiIndex.from_product([['noisy', 'quiet', 'overall'], 
                                          ['fixations_on_face', 'saccades', 'blinks'], 
                                          ['quantity', 'duration']])
    df = pd.DataFrame(columns=columns)

    for participant in os.listdir(base_path):
        participant_path = os.path.join(base_path, participant)
        if os.path.isdir(participant_path):
            data = {'noisy': {'fixations_on_face': {'quantity': 0, 'duration': 0},
                              'saccades': {'quantity': 0, 'duration': 0},
                              'blinks': {'quantity': 0, 'duration': 0}},
                    'quiet': {'fixations_on_face': {'quantity': 0, 'duration': 0},
                              'saccades': {'quantity': 0, 'duration': 0},
                              'blinks': {'quantity': 0, 'duration': 0}},
                    'overall': {'fixations_on_face': {'quantity': 0, 'duration': 0},
                                'saccades': {'quantity': 0, 'duration': 0},
                                'blinks': {'quantity': 0, 'duration': 0}}}

            for file_name in ['fixations_on_face.csv', 'saccades.csv', 'blinks.csv']:
                file_path = os.path.join(participant_path, file_name)
                if os.path.exists(file_path):
                    df_file = pd.read_csv(file_path)
                    data_type = file_name.split('.')[0]
                    for trial_type in ['noisy', 'quiet']:
                        trial_data = df_file[df_file['trial_type'] == trial_type]
                        data[trial_type][data_type]['quantity'] = len(trial_data)
                        data[trial_type][data_type]['duration'] = ((trial_data['end timestamp [ns]'] - trial_data['start timestamp [ns]']).mean()) / 1e9
                    data['overall'][data_type]['quantity'] = len(df_file)
                    data['overall'][data_type]['duration'] = ((df_file['end timestamp [ns]'] - df_file['start timestamp [ns]']).mean()) / 1e9

            df.loc[participant] = [data['noisy']['fixations_on_face']['quantity'], data['noisy']['fixations_on_face']['duration'],
                                   data['noisy']['saccades']['quantity'], data['noisy']['saccades']['duration'],
                                   data['noisy']['blinks']['quantity'], data['noisy']['blinks']['duration'],
                                   data['quiet']['fixations_on_face']['quantity'], data['quiet']['fixations_on_face']['duration'],
                                   data['quiet']['saccades']['quantity'], data['quiet']['saccades']['duration'],
                                   data['quiet']['blinks']['quantity'], data['quiet']['blinks']['duration'],
                                   data['overall']['fixations_on_face']['quantity'], data['overall']['fixations_on_face']['duration'],
                                   data['overall']['saccades']['quantity'], data['overall']['saccades']['duration'],
                                   data['overall']['blinks']['quantity'], data['overall']['blinks']['duration']]

    df.loc['average'] = df.mean()
    df.loc['std_dev'] = df.std()

    return df

def dataframe_by_trial_id():
    base_path = r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Raw_Data\participants'
    trial_ids = set()
    
    # Collect all unique trial IDs
    for participant in os.listdir(base_path):
        participant_path = os.path.join(base_path, participant)
        if os.path.isdir(participant_path):
            for file_name in ['fixations_on_face.csv', 'saccades.csv', 'blinks.csv']:
                file_path = os.path.join(participant_path, file_name)
                if os.path.exists(file_path):
                    df_file = pd.read_csv(file_path)
                    trial_ids.update(df_file['trial_id'].unique())

    trial_ids = sorted(trial_ids)
    columns = pd.MultiIndex.from_product([trial_ids, 
                                          ['fixations_on_face', 'saccades', 'blinks'], 
                                          ['quantity', 'duration']])
    trial_df = pd.DataFrame(columns=columns)

    for participant in os.listdir(base_path):
        participant_path = os.path.join(base_path, participant)
        if os.path.isdir(participant_path):
            data = {trial_id: {'fixations_on_face': {'quantity': 0, 'duration': 0},
                               'saccades': {'quantity': 0, 'duration': 0},
                               'blinks': {'quantity': 0, 'duration': 0}} for trial_id in trial_ids}

            for file_name in ['fixations_on_face.csv', 'saccades.csv', 'blinks.csv']:
                file_path = os.path.join(participant_path, file_name)
                if os.path.exists(file_path):
                    df_file = pd.read_csv(file_path)
                    data_type = file_name.split('.')[0]
                    for trial_id in trial_ids:
                        trial_data = df_file[df_file['trial_id'] == trial_id]
                        if not trial_data.empty:
                            data[trial_id][data_type]['quantity'] = len(trial_data)
                            data[trial_id][data_type]['duration'] = ((trial_data['end timestamp [ns]'] - trial_data['start timestamp [ns]']).mean()) / 1e9

            trial_df.loc[participant] = [item for trial_id in trial_ids for item in 
                                         (data[trial_id]['fixations_on_face']['quantity'], data[trial_id]['fixations_on_face']['duration'],
                                          data[trial_id]['saccades']['quantity'], data[trial_id]['saccades']['duration'],
                                          data[trial_id]['blinks']['quantity'], data[trial_id]['blinks']['duration'])]

    trial_df.loc['average'] = trial_df.mean()
    trial_df.loc['std_dev'] = trial_df.std()

    # Ensure the Clean_data directory exists
    clean_data_dir = r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Clean_data'
    os.makedirs(clean_data_dir, exist_ok=True)
    
    # Save the trial DataFrame
    trial_df.to_csv(os.path.join(clean_data_dir, 'trial_summary.csv'), index=False)

    return trial_df

# running the functions
df = process_all_subjects_noisy_and_quiet()
df.to_csv(r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Clean_data\summary.csv')

trial_df = dataframe_by_trial_id()
trial_df.to_csv(r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Clean_data\trial_summary.csv')


