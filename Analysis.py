import pandas as pd

tabMovieTitles = pd.read_csv("Data/MovieTitles.csv", sep="|", encoding="ISO-8859-1", header=None)
print(tabMovieTitles.shape)

tabMovieCharacters = pd.read_csv("Data/MovieCharacters.csv", sep="|", encoding="ISO-8859-1", header=None)
print(tabMovieCharacters.shape)

tabMovieLines = pd.read_csv("Data/MovieLines.csv", sep="|", encoding="ISO-8859-1", header=None)
print(tabMovieLines.shape)

tabMovieConversations = pd.read_csv("Data/MovieConversations.csv", sep="|", encoding="ISO-8859-1", header=None)
print(tabMovieConversations.shape)

tabMovieRawScriptURLs = pd.read_csv("Data/MovieRawScriptURLs.csv", sep="|", encoding="ISO-8859-1", header=None)
print(tabMovieRawScriptURLs.shape)