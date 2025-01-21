import os

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

# def combine_Raw_data_files():
#     """
#     Combine all the files in the Raw_data folder into one file for each variable.
#     """
#     raw_data_folder = r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Raw_data'
#     clean_data_folder = r'C:\Users\USER\Desktop\Advanced Python Course\Python Project\data\Clean_data'
    
#     for variable in ['blinks', 'saccades', 'fixations_on_face']:
#         combined_df = pd.DataFrame()
#         for file_name in os.listdir(os.path.join(raw_data_folder, variable)):
#             file_path = os.path.join(raw_data_folder, variable, file_name)
#             df = pd.read_csv(file_path)
#             combined_df = pd.concat([combined_df, df])
#         combined_df.to_csv(os.path.join(clean_data_folder, variable, f'{variable}.csv'), index=False)
