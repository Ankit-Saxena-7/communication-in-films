import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.pyplot import xticks

tabMovieLines = pd.read_csv("Data/MovieLines.csv", sep="|", encoding="ISO-8859-1", header=None, names=["Line ID", "Character ID", "Movie ID", "Character Name", "Dialogue"])

tabMovieCharacters = pd.read_csv("Data/MovieCharacters.csv", sep="|", encoding="ISO-8859-1", header=None, names=["Character ID", "Character Name", "Movie ID", "Movie Title", "Gender", "Position"])

tabMovieLinesFull = pd.merge(tabMovieLines, tabMovieCharacters[['Character ID', 'Character Name', 'Gender', 'Position']], on='Character ID')

tabMovieLinesFull = tabMovieLinesFull.drop(['Character Name_x'], axis=1)
tabMovieLinesFull = tabMovieLinesFull.rename(columns = {'Character Name_y': 'Character Name'})
print(tabMovieLinesFull.columns)

tabMovieTitles = pd.read_csv("Data/MovieTitles.csv", sep="|", encoding="ISO-8859-1", header=None, names=["Movie ID", "Movie Title", "Year", "IMDb Rating", "IMDb Votes", "Genres"])

tabMovieTitles['Year'] = tabMovieTitles['Year'].map(lambda x: x.rstrip('/I'))
tabMovieTitles['Year'] = pd.to_datetime(tabMovieTitles['Year'], format='%Y')

tabMovieLinesFull = pd.merge(tabMovieLinesFull, tabMovieTitles, on='Movie ID')
print(tabMovieLinesFull.columns)

tabMovieConversations = pd.read_csv("Data/MovieConversations.csv", encoding="ISO-8859-1", sep="|", header=None, names=["ID First", "ID Second", "Movie ID", "Conversation"])
print(tabMovieConversations.head())

tabMovieRawScriptURLs = pd.read_csv("Data/MovieRawScriptURLs.csv", encoding="ISO-8859-1", sep="|", header=None, names=["Movie ID", "Movie Title", "Raw Script URL"])

tabMovieLinesFull = pd.merge(tabMovieLinesFull, tabMovieRawScriptURLs[['Movie ID', 'Raw Script URL']], on='Movie ID')

tabMovieLinesFull = tabMovieLinesFull.set_index('Line ID')

print("SHAPE")
print(tabMovieLinesFull.shape)

# Merging complete

tabMovieLinesFull.loc[tabMovieLinesFull['Gender'] == 'M', 'Gender'] = 'm'
tabMovieLinesFull.loc[tabMovieLinesFull['Gender'] == 'F', 'Gender'] = 'f'

print(tabMovieLinesFull.columns)

# Grouping By Gender
tabMovieLinesFull['Release Year'] = pd.DatetimeIndex(tabMovieLinesFull['Year']).year

YearlyDialogues = tabMovieLinesFull.groupby('Release Year').agg({
    'Dialogue': ['count']
    })

tabMovieLinesFull['Dialogue Length'] = tabMovieLinesFull['Dialogue'].str.len()
tabMovieLinesFull['Dialogue Words'] = tabMovieLinesFull['Dialogue'].str.split().str.len()

tabGenderGroups = tabMovieLinesFull[tabMovieLinesFull.Gender != '?'].groupby('Gender').agg({
    'Character ID':['nunique'],
    'Dialogue Length':['sum', 'mean'],
    'Dialogue Words':['sum', 'mean']
     })

tabGenderGroups.reset_index(inplace=True)

tabGenderGroups.columns = ['Gender', 'Total Characters', 'Cumulative Sentence Length', 'Avg Sentence Length', 'Cumulative Words', 'Avg Words Per Sentence']

print(tabGenderGroups)

# VISUALIZATIONS

# Yearly Dialogues
YearlyDialogues.columns = ['Total Dialogues']

print(YearlyDialogues.head())

YearlyDialogues.reset_index(inplace=True)

plt.bar(YearlyDialogues['Release Year'], YearlyDialogues['Total Dialogues'], align='center')
locations, labels = xticks()
plt.xlabel('Release Year')
plt.ylabel('Total Dialogues')
plt.title('Dialogues Across Release Years')
plt.xticks(locations, labels)
plt.show()


# Yearly Movies
YearlyMovies = tabMovieLinesFull.groupby('Release Year').agg({
    'Movie ID': [pd.Series.nunique]
    })

YearlyMovies.columns = ['Total Movies']

print(YearlyMovies.head())

YearlyMovies.reset_index(inplace=True)

plt.bar(YearlyMovies['Release Year'], YearlyMovies['Total Movies'], align='center')
locations, labels = xticks()
plt.xlabel('Release Year')
plt.ylabel('Total Movies')
plt.title('Movies Across Release Years')
plt.xticks(locations, labels)
plt.show()

# Genders

plt.bar(tabGenderGroups['Gender'], tabGenderGroups['Total Characters'], align='center', width=0.4)
locations, labels = xticks()
plt.xlabel('Gender')
plt.ylabel('Total Characters')
plt.title('Character Genders')
plt.xticks(locations, ['Female', 'Males'])
plt.show()

# Cumulative Sentence Length

plt.bar(tabGenderGroups['Gender'], tabGenderGroups['Cumulative Sentence Length'], align='center', width=0.4)
locations, labels = xticks()
plt.xlabel('Gender')
plt.ylabel('Total Characters')
plt.title('Cumulative Sentence Length For Genders')
plt.xticks(locations, ['Female', 'Males'])
plt.show()

# Avg Sentence Length

plt.bar(tabGenderGroups['Gender'], tabGenderGroups['Avg Sentence Length'], align='center', width=0.4)
locations, labels = xticks()
plt.xlabel('Gender')
plt.ylabel('Total Characters')
plt.title('Average Sentence Length For Genders')
plt.xticks(locations, ['Female', 'Males'])
plt.show()

# Cumulative Words

plt.bar(tabGenderGroups['Gender'], tabGenderGroups['Cumulative Words'], align='center', width=0.4)
locations, labels = xticks()
plt.xlabel('Gender')
plt.ylabel('Total Words')
plt.title('Cumulative Words For Genders')
plt.xticks(locations, ['Female', 'Males'])
plt.show()

# Avg Words Per Sentence

plt.bar(tabGenderGroups['Gender'], tabGenderGroups['Avg Words Per Sentence'], align='center', width=0.4)
locations, labels = xticks()
plt.xlabel('Gender')
plt.ylabel('Total Words')
plt.title('Average Words Per Sentence For Genders')
plt.xticks(locations, ['Female', 'Males'])
plt.show()
