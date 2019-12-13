import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.pyplot import xticks
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

tabMovieLines = pd.read_csv("Data/MovieLines.csv", sep="|", encoding="ISO-8859-1", header=None,
                            names=["Line ID", "Character ID", "Movie ID", "Character Name", "Dialogue"])

tabMovieCharacters = pd.read_csv("Data/MovieCharacters.csv", sep="|", encoding="ISO-8859-1", header=None,
                                 names=["Character ID", "Character Name", "Movie ID", "Movie Title", "Gender",
                                        "Position"])

tabMovieLinesFull = pd.merge(tabMovieLines,
                             tabMovieCharacters[['Character ID', 'Character Name', 'Gender', 'Position']],
                             on='Character ID')

tabMovieLinesFull = tabMovieLinesFull.drop(['Character Name_x'], axis=1)
tabMovieLinesFull = tabMovieLinesFull.rename(columns={'Character Name_y': 'Character Name'})

tabMovieTitles = pd.read_csv("Data/MovieTitles.csv", sep="|", encoding="ISO-8859-1", header=None,
                             names=["Movie ID", "Movie Title", "Year", "IMDb Rating", "IMDb Votes", "Genres"])

tabMovieTitles['Year'] = tabMovieTitles['Year'].map(lambda x: x.rstrip('/I'))
tabMovieTitles['Year'] = pd.to_datetime(tabMovieTitles['Year'], format='%Y')

tabMovieLinesFull = pd.merge(tabMovieLinesFull, tabMovieTitles, on='Movie ID')

tabMovieConversations = pd.read_csv("Data/MovieConversations.csv", encoding="ISO-8859-1", sep="|", header=None,
                                    names=["ID First", "ID Second", "Movie ID", "Conversation"])
print(tabMovieConversations.head())

tabMovieRawScriptURLs = pd.read_csv("Data/MovieRawScriptURLs.csv", encoding="ISO-8859-1", sep="|", header=None,
                                    names=["Movie ID", "Movie Title", "Raw Script URL"])

tabMovieLinesFull = pd.merge(tabMovieLinesFull, tabMovieRawScriptURLs[['Movie ID', 'Raw Script URL']], on='Movie ID')

tabMovieLinesFull = tabMovieLinesFull.set_index('Line ID')


# Merging complete

tabMovieLinesFull.loc[tabMovieLinesFull['Gender'] == 'M', 'Gender'] = 'm'
tabMovieLinesFull.loc[tabMovieLinesFull['Gender'] == 'F', 'Gender'] = 'f'

print('\n')
print('tabMovieLinesFull: ')
print(tabMovieLinesFull.columns)
print('\n')

# Grouping By Gender
tabMovieLinesFull['Release Year'] = pd.DatetimeIndex(tabMovieLinesFull['Year']).year

YearlyDialogues = tabMovieLinesFull.groupby('Release Year').agg({
    'Dialogue': ['count']
})

tabMovieLinesFull['Dialogue Length'] = tabMovieLinesFull['Dialogue'].str.len()
tabMovieLinesFull['Dialogue Words'] = tabMovieLinesFull['Dialogue'].str.split().str.len()

tabGenderGroups = tabMovieLinesFull[tabMovieLinesFull.Gender != '?'].groupby('Gender').agg({
    'Character ID': ['nunique'],
    'Dialogue Length': ['sum', 'mean'],
    'Dialogue Words': ['sum', 'mean']
})

tabGenderGroups.reset_index(inplace=True)

tabGenderGroups.columns = ['Gender', 'Total Characters', 'Cumulative Sentence Length', 'Avg Sentence Length',
                           'Cumulative Words', 'Avg Words Per Sentence']

print(tabGenderGroups)

# VISUALIZATIONS
"""
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
# plt.show()


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
# plt.show()

# Genders

plt.bar(tabGenderGroups['Gender'], tabGenderGroups['Total Characters'], align='center', width=0.4)
locations, labels = xticks()
plt.xlabel('Gender')
plt.ylabel('Total Characters')
plt.title('Character Genders')
plt.xticks(locations, ['Female', 'Males'])
# plt.show()

# Cumulative Sentence Length

plt.bar(tabGenderGroups['Gender'], tabGenderGroups['Cumulative Sentence Length'], align='center', width=0.4)
locations, labels = xticks()
plt.xlabel('Gender')
plt.ylabel('Total Characters')
plt.title('Cumulative Sentence Length For Genders')
plt.xticks(locations, ['Female', 'Males'])
# plt.show()

# Avg Sentence Length

plt.bar(tabGenderGroups['Gender'], tabGenderGroups['Avg Sentence Length'], align='center', width=0.4)
locations, labels = xticks()
plt.xlabel('Gender')
plt.ylabel('Total Characters')
plt.title('Average Sentence Length For Genders')
plt.xticks(locations, ['Female', 'Males'])
# plt.show()

# Cumulative Words

plt.bar(tabGenderGroups['Gender'], tabGenderGroups['Cumulative Words'], align='center', width=0.4)
locations, labels = xticks()
plt.xlabel('Gender')
plt.ylabel('Total Words')
plt.title('Cumulative Words For Genders')
plt.xticks(locations, ['Female', 'Males'])
# plt.show()

# Avg Words Per Sentence

plt.bar(tabGenderGroups['Gender'], tabGenderGroups['Avg Words Per Sentence'], align='center', width=0.4)
locations, labels = xticks()
plt.xlabel('Gender')
plt.ylabel('Total Words')
plt.title('Average Words Per Sentence For Genders')
plt.xticks(locations, ['Female', 'Males'])
# plt.show()
"""

# SENTIMENT ANALYSIS

vVaderAnalyser = SentimentIntensityAnalyzer()


def SentimentAnalyzerScores(pDialogue):
    vScore = vVaderAnalyser.polarity_scores(pDialogue)
    return dict(vScore)


tabMovieLinesFull['Dialogue'] = tabMovieLinesFull['Dialogue'].astype(str)

tabMovieLinesFull['Sentiment'] = tabMovieLinesFull.apply(lambda vRow: SentimentAnalyzerScores(vRow['Dialogue']), axis=1)

DFSentiment = pd.DataFrame(list(tabMovieLinesFull['Sentiment']))

DFSentiment.columns = ['Sentiment Negative', 'Sentiment Neutral', 'Sentiment Positive', 'Sentiment Compound']

tabMovieLinesFull.reset_index(inplace=True)

tabMovieLinesFull = pd.concat([tabMovieLinesFull, DFSentiment], axis=1)

tabMovieLinesFull.drop(['Sentiment'], axis=1, inplace=True)

# EMOTION ANALYSIS
'''
from liwc import Liwc

liwc = Liwc('LIWC2007_English100131.dic')
# Search a word in the dictionary to find in which LIWC categories it belongs
print(liwc.search('happy'))

print(liwc.parse('I counted on you to help my cause. You and that thug are obviously failing. Aren\'t we ever going on our date?'.split(' ')))

tabMovieLinesFull['Linguistics'] = tabMovieLinesFull.apply(lambda vRow: liwc.parse(vRow['Dialogue']), axis=1)

print(tabMovieLinesFull['Linguistics'].head())

tabMovieLinesFull.to_csv('tabMovieLinesFull.csv', sep=',', encoding='utf-8')
'''

'''
tabMovieConversations = pd.read_csv("Data/tabMovieConversations.csv", encoding="ISO-8859-1", sep=",", header=None, names=["ID First", "ID Second", "Movie ID", "Conversation", "Conversation Starter"])
print(tabMovieConversations.head())
'''


# Yearly ratio
tabMovieLinesFull['Year'] = pd.DatetimeIndex(tabMovieLinesFull['Year']).year
tabYearlyGenderCount = tabMovieLinesFull.loc[tabMovieLinesFull.Gender != '?'].groupby(['Year' , 'Gender']).size()
tabYearlyGenderPercentages = tabYearlyGenderCount.groupby(level=0).apply(lambda x: x/float(x.sum()))

# DOWNLOAD
tabYearlyGenderCount.to_csv('OUTtabYearlyGenderCount.csv', sep=',', encoding='utf-8')
tabMovieConversations.to_csv('OUTtabMovieConversations.csv', sep=',', encoding='utf-8')
tabGenderGroups.to_csv('OUTtabGenderGroups.csv', sep=',', encoding='utf-8')
tabMovieLinesFull.to_csv('OUTtabMovieLinesFull.csv', sep=',', encoding='utf-8')

tabYearlyGenderPercentages.to_csv('OUTtabYearlyGenderPercentages.csv', sep=',', encoding='utf-8')




