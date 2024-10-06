import pandas as pd
import utils
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, recall_score, classification_report, precision_score, confusion_matrix


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

data_frames = utils.load_dataframes(data_dir, csv_files)

qualified_teams_10 = utils.get_qualified_teams(data_frames['teams'], 10)

print("\nTeams that qualified for the playoffs in year 10:")
print(qualified_teams_10['tmID'].head(8))

# Convert the diagnosis column to binary
data_frames['teams']['playoff'] = data_frames['teams']['playoff'].map({'Y': 1, 'N': 0})
	
# Split the dataset into features and labels
features = data_frames['teams'].drop(['playoff'],axis=1) 
labels = data_frames['teams']['playoff']

# Split the data into training and test sets with stratified sampling
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42, stratify=labels)

# Print the shapes of the training and test sets
print("Training set shape:", X_train.shape, y_train.shape)
print("Test set shape:", X_test.shape, y_test.shape)
