import pandas as pd
import os


def load_dataframes(data_dir, csv_files):
    data_frames = {}
    for name, file in csv_files.items():
        file_path = os.path.join(data_dir, file)
        data_frames[name] = pd.read_csv(file_path)
        print(f"\n{name} DataFrame:")
        print(data_frames[name].head())
    return data_frames

# get the teams that made it to the playoffs that year
def get_qualified_teams(df, year):
    return df[(df['year'] == year) & (df['playoff'] == 'Y')].sort_values(by='rank')
    