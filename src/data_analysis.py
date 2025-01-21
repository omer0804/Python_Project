import os
import pandas as pd

# Calculate the average for each experimenter and each variable
def create_clean_data_folder():
    r"""create a folder for Clean_data in C:\Users\USER\Desktop\Advanced Python Course\Python Project\data
    inside it we will have 3 folders: blinks, saccaades, fixations on face, skip it if it already exists
    """
    clean_data_folder = r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Clean_data'
    if not os.path.exists(clean_data_folder):
        os.mkdir(clean_data_folder)
        os.mkdir(os.path.join(clean_data_folder, 'blinks'))
        os.mkdir(os.path.join(clean_data_folder, 'saccades'))
        os.mkdir(os.path.join(clean_data_folder, 'fixations_on_face'))
    else:
        print('Clean_data folder already exists.')
    
# running the function
create_clean_data_folder()

def process_all_subjects_globally():
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

# running the function
create_clean_data_folder()
df = process_all_subjects_globally()
df.to_csv(r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Clean_data\summary.csv')
print(df)