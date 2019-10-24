import pandas as pd

#tabMovieCharacters = pd.read_csv("Data/MovieCharacters.csv", sep="|", encoding="ISO-8859-1", header=None, names=["Character ID", "Character Name", "Movie ID", "Movie Title", "Gender", "Position"], index_col='Character ID')
#print(tabMovieCharacters.Gender.unique())
#print(tabMovieCharacters.loc[tabMovieCharacters.Gender == '?', ["Gender", "Character Name"]])

#tabMovieRawScriptURLs = pd.read_csv("Data/MovieRawScriptURLs.csv", sep="|", encoding="ISO-8859-1", header=None)
#print(tabMovieRawScriptURLs.shape)

tabMovieLines = pd.read_csv("Data/MovieLines.csv", sep="|", encoding="ISO-8859-1", header=None, names=["Line ID", "Character ID", "Movie ID", "Character Name", "Dialogue"])
#print(tabMovieLines.head())
tabMovieCharacters = pd.read_csv("Data/MovieCharacters.csv", sep="|", encoding="ISO-8859-1", header=None, names=["Character ID", "Character Name", "Movie ID", "Movie Title", "Gender", "Position"])
#print(tabMovieCharacters.head())

merged = pd.merge(tabMovieLines, tabMovieCharacters[['Character ID', 'Character Name', 'Gender', 'Position']], on='Character ID')

merged = merged.drop(['Character Name_x'], axis=1)
merged = merged.rename(columns = {'Character Name_y': 'Character Name'})
print(merged.columns)

tabMovieTitles = pd.read_csv("Data/MovieTitles.csv", sep="|", encoding="ISO-8859-1", header=None, names=["Movie ID", "Movie Title", "Year", "IMDb Rating", "IMDb Votes", "Genres"])

#print(tabMovieTitles.loc[tabMovieTitles['Year'] == '1989/I']["Movie Title"])
#print(tabMovieTitles.loc[tabMovieTitles.Year.str.contains('/I'), ["Year", "Movie Title"]])
#print(tabMovieTitles.Year.str.contains('/I'))
tabMovieTitles['Year'] = tabMovieTitles['Year'].map(lambda x: x.rstrip('/I'))
tabMovieTitles['Year'] = pd.to_datetime(tabMovieTitles['Year'], format='%Y')

merged2 = pd.merge(merged, tabMovieTitles, on='Movie ID')
print(merged2.columns)

tabMovieConversations = pd.read_csv("Data/MovieConversations.csv", encoding="ISO-8859-1", sep="|", header=None, names=["ID First", "ID Second", "Movie ID", "Conversation"])
print(tabMovieConversations.head())

tabMovieRawScriptURLs = pd.read_csv("Data/MovieRawScriptURLs.csv", encoding="ISO-8859-1", sep="|", header=None, names=["Movie ID", "Movie Title", "Raw Script URL"])

tabMovieLinesFull = pd.merge(merged2, tabMovieRawScriptURLs[['Movie ID', 'Raw Script URL']], on='Movie ID')

tabMovieLinesFull = tabMovieLinesFull.set_index('Line ID')

print(tabMovieLinesFull.shape)



# Merging complete
