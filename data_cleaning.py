import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


data_dir = 'data'

csv_files = {
    'awards_players': 'awards_players.csv',
    'coaches': 'coaches.csv',
    'players': 'players.csv',
    'players_teams': 'players_teams.csv',
    'series_post': 'series_post.csv',
    'teams': 'teams.csv',
    'teams_post': 'teams_post.csv'
}


data_frames = {}
for name, file in csv_files.items():
    file_path = os.path.join(data_dir, file)
    data_frames[name] = pd.read_csv(file_path)
    # print(f"\n{name} DataFrame:")
    # print(data_frames[name].head())


def check_missing_values(dfs):
    for name,df in dfs.items():
        print(name, ":")
        print(df.isnull().sum())

def handle_duplicates(dfs):
    for name,df in dfs.items():
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            print("{duplicates} rows duplicated in {name}")
            # remove (no need there are none)

output_dir = 'cleaned_data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#clean awards_players.csv

awards_df = data_frames['awards_players']


awards_df = awards_df.iloc[:, :-1]  # Drop the last column

#Add the missing "award" value for line 30
awards_df.at[28, 'award'] = "Kim Perrot Sportsmanship Award" 


output_file = 'modified_awards_players.csv'
 #Save the modified DataFrame to a CSV file in the specified directory
awards_df.to_csv(os.path.join(output_dir, output_file), index=False)

#clean players_teams.csv

players_teams_df = data_frames['players_teams']


players_teams_df = players_teams_df.drop(players_teams_df.columns[4], axis=1)

#drop 11th column and 29th column 
players_teams_df = players_teams_df.drop(players_teams_df.columns[10], axis=1)
players_teams_df = players_teams_df.drop(players_teams_df.columns[28], axis=1)
output_file = 'modified_players_teams.csv'
 #Save the modified DataFrame to a CSV file in the specified directory
players_teams_df.to_csv(os.path.join(output_dir, output_file), index=False)


#clean coaches.csv

coaches_df = data_frames['coaches']
coaches_df = coaches_df.drop(coaches_df.columns[3], axis=1)

output_file = 'modified_coaches.csv'

coaches_df.to_csv(os.path.join(output_dir, output_file), index=False)

#clean players.csv

players_df = data_frames['players']
#drop 3rd and 4th and 6th columns
players_df = players_df.drop(players_df.columns[[2, 3,7]], axis=1)

#drop last column
players_df = players_df.iloc[:, :-1]
output_file = 'modified_players.csv'

players_df.to_csv(os.path.join(output_dir, output_file), index=False)

#clean series_post.csv

series_post_df = data_frames['series_post']

series_post_df = series_post_df.drop(series_post_df.columns[[4,6]] , axis=1)


output_file = 'modified_series_post.csv'

series_post_df.to_csv(os.path.join(output_dir, output_file), index=False)

#clean teams post

teams_post_df = data_frames['teams_post']

teams_post_df = teams_post_df.drop(teams_post_df.columns[2], axis=1)

output_file = 'modified_teams_post.csv'

teams_post_df.to_csv(os.path.join(output_dir, output_file), index=False)

#clean teams.csv

teams_df = data_frames['teams']

teams_df = teams_df.drop(teams_df.columns[[1,3,5,8,12,43,44,45,46,47,48,49,51]], axis=1)

output_file = 'modified_teams.csv'

teams_df.to_csv(os.path.join(output_dir, output_file), index=False)


import matplotlib.pyplot as plt

# Function to create a histogram for numerical data
def plot_histogram(df, column, bins=50):
    plt.figure(figsize=(10, 6))
    plt.hist(df[column], bins=bins, color='skyblue', edgecolor='black')
    plt.title(f'Histogram of {column.capitalize()}')
    plt.xlabel(f'{column.capitalize()}')
    plt.ylabel('Frequency')
    plt.show()

 # Example: Plot a histogram  to check for outliers
#plot_histogram(data_frames['teams'], 'seeded')

# handle_duplicates(data_frames)

#check_missing_values(data_frames)