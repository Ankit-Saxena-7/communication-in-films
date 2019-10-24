import pandas as pd

#print(tabMovieCharacters.Gender.unique())
#print(tabMovieCharacters.loc[tabMovieCharacters.Gender == '?', ["Gender", "Character Name"]])

tabMovieLines = pd.read_csv("Data/MovieLines.csv", sep="|", encoding="ISO-8859-1", header=None, names=["Line ID", "Character ID", "Movie ID", "Character Name", "Dialogue"])

tabMovieCharacters = pd.read_csv("Data/MovieCharacters.csv", sep="|", encoding="ISO-8859-1", header=None, names=["Character ID", "Character Name", "Movie ID", "Movie Title", "Gender", "Position"])

merged1 = pd.merge(tabMovieLines, tabMovieCharacters[['Character ID', 'Character Name', 'Gender', 'Position']], on='Character ID')

merged1 = merged1.drop(['Character Name_x'], axis=1)
merged1 = merged1.rename(columns = {'Character Name_y': 'Character Name'})
print(merged1.columns)

tabMovieTitles = pd.read_csv("Data/MovieTitles.csv", sep="|", encoding="ISO-8859-1", header=None, names=["Movie ID", "Movie Title", "Year", "IMDb Rating", "IMDb Votes", "Genres"])

tabMovieTitles['Year'] = tabMovieTitles['Year'].map(lambda x: x.rstrip('/I'))
tabMovieTitles['Year'] = pd.to_datetime(tabMovieTitles['Year'], format='%Y')

merged1 = pd.merge(merged1, tabMovieTitles, on='Movie ID')
print(merged1.columns)

tabMovieConversations = pd.read_csv("Data/MovieConversations.csv", encoding="ISO-8859-1", sep="|", header=None, names=["ID First", "ID Second", "Movie ID", "Conversation"])
print(tabMovieConversations.head())

tabMovieRawScriptURLs = pd.read_csv("Data/MovieRawScriptURLs.csv", encoding="ISO-8859-1", sep="|", header=None, names=["Movie ID", "Movie Title", "Raw Script URL"])

merged1 = pd.merge(merged1, tabMovieRawScriptURLs[['Movie ID', 'Raw Script URL']], on='Movie ID')

merged1 = merged1.set_index('Line ID')

print("SHAPE")
print(merged1.shape)

# Merging complete

print(tabMovieCharacters.Gender.value_counts())

tabMovieCharacters.loc[tabMovieCharacters['Gender'] == 'M', 'Gender'] = 'm'
tabMovieCharacters.loc[tabMovieCharacters['Gender'] == 'F', 'Gender'] = 'f'

print(tabMovieCharacters.Gender.value_counts())