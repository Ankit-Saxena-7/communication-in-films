import pandas as pd

#tabMovieTitles = pd.read_csv("Data/MovieTitles.csv", sep="|", encoding="ISO-8859-1", header=None, names=["Movie ID", "Movie Title", "Year", "IMDb Rating", "IMDb Votes", "Genres"])
#tabMovieTitles = tabMovieTitles.set_index("Movie ID")
#print(tabMovieTitles.loc[tabMovieTitles['Year'] == '1989/I']["Movie Title"])
#print(tabMovieTitles.loc[tabMovieTitles.Year.str.contains('/I'), ["Year", "Movie Title"]])
#print(tabMovieTitles.Year.str.contains('/I'))
#tabMovieTitles['Year'] = tabMovieTitles['Year'].map(lambda x: x.rstrip('/I'))
#tabMovieTitles['Year'] = pd.to_datetime(tabMovieTitles['Year'], format='%Y')
#print(tabMovieTitles.head())




tabMovieCharacters = pd.read_csv("Data/MovieCharacters.csv", sep="|", encoding="ISO-8859-1", header=None, names=["Character ID", "Character Name", "Movie ID", "Movie Title", "Gender", "Position"])
tabMovieCharacters = tabMovieCharacters.set_index("Character ID")
print(tabMovieCharacters.info())
print(tabMovieCharacters.Gender.unique())

print(tabMovieCharacters.loc[tabMovieCharacters.Gender == '?', ["Gender", "Character Name"]])



#tabMovieLines = pd.read_csv("Data/MovieLines.csv", sep="|", encoding="ISO-8859-1", header=None)
#print(tabMovieLines.shape)
#print(tabMovieLines.columns)
#tabMovieConversations = pd.read_csv("Data/MovieConversations.csv", sep="|", encoding="ISO-8859-1", header=None)
#print(tabMovieConversations.shape)

#tabMovieRawScriptURLs = pd.read_csv("Data/MovieRawScriptURLs.csv", sep="|", encoding="ISO-8859-1", header=None)
#print(tabMovieRawScriptURLs.shape)

#print(tabMovieLines.columns)
#print(df['Borough'].value_counts(dropna=False))

