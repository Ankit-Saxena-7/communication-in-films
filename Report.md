---
title: "Discovering Patterns in Film Dialogues"
author: Ankit Saxena
output:
  html_document:
    keep_md: true
---

### Introduction

Effective dialogue between movie characters is one of the most important tools a filmmaker has to communicate the vision of their movie, move the plot forward, and engage the audience. Analyzing conversations between different movie characters can uncover the quantitative and qualitative differences between dialogues across different films and also uncover any forms of bias (like gender bias) that may exist in these conversations.

### The Data

The data set has been been extracted by the Cornell Movie - Dialogs Corpus that contains 220,579 conversational exchanges between 9,035 characters from 617 movies. In total, there are 304,713 dialogues taken from raw movie scripts. The entire data set is available in Kaggle's website and can be accessed through this [link](https://www.kaggle.com/rajathmc/cornell-moviedialog-corpus).

The data has been systematically organized into five different tables in CSV format. Their contents are described below:

* _MovieTitles.csv_: Information about each movie title uniquely identified by the Movie ID column

* _MovieCharacters.csv_: All movie characters uniquely identified by the Character ID column

* _MovieLines.csv_: The actual text of each dialogue spoken uniquely identified by the Line ID column

* _MovieConversations.csv_: The structure of all conversations uniquely identified by the Character ID of the first character in the conversation, Character ID of the second character, and the Movie ID column

* _MovieRawScriptURL.csv_: The uniform resource locator (URL) of all the raw scripts

### Repository Structure

The folders in the repository are organized as follows:

* _communication-in-films_: Root folder
  + _Dialogues.mb_: The Markdown file for this project
  + _Data_
    + _MovieTitles.csv_
    + _MovieCharacters.csv_
    + _MovieLines.csv_
    + _MovieConversations.csv_
    + _MovieRawScriptURLs.csv_

#### Entity Relationship Diagram

The tables are related in the following manner:

<img src="Assets/ERD.png"
     alt="ERD"
     style="width: 800px; height: 300px;" />

### Coding Standards

* Entities like variables and functions have been named using camel case convention
* Local variables have been prefixed using 'v'
* Tables have been prefixed using 'tab'

### Data Cleaning (Pre-load)

The following steps were performed on the _MovieLines.csv_ file when cleaning the data:
* The default delimiter from the data source was this combination of characters: ' +++$+++ '. This has been changed to the pipe character '|'.
* Column five in _MovieLines.csv_ has spurious pipe characters which will interfere with the data loading step. Those have been deleted without a loss of valuable data.
* There is one spurious caret character '^' as a number separator. That has been removed without interfering with the number.
* To express emphasis on certain words, certain HTML tags have been used (like '\<i\> ... \</i\>','\<u\> ... \</u\>', '\<b\> ... \</b\>', '\<html\> ... \</html\>, '\<pre\> ... \</pre\>'), which can interfere with our analysis. Those have been removed as that information is not relevant to our analysis.

Once these steps are completed, we are left with 303,249 lines of dialogues.

### Importing Packages

The following packages will need to be imported for the analysis:

```python
# Using dataframes
import pandas as pd

# Plotting charts
from matplotlib import pyplot as plt
from matplotlib.pyplot import xticks

# Analyzing sentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
```

### Importing the Data

Run the following scripts to import the data from your repository and check the dimensions of each table to makes sure the complete set has been loaded.

__Movie Titles__

```python
tabMovieTitles = pd.read_csv("Data/MovieTitles.csv", sep="|", encoding="ISO-8859-1", header=None, names=["Movie ID", "Movie Title", "Year", "IMDb Rating", "IMDb Votes", "Genres"])
```

Table shape
```python
print(tabMovieTitles.shape)
```

Table columns
```python
print(tabMovieTitles.columns)
```

Table information
```python
print(tabMovieTitles.info())
```

__Movie Characters__

```python
tabMovieCharacters = pd.read_csv("Data/MovieCharacters.csv", sep="|", encoding="ISO-8859-1", header=None, names=["Character ID", "Character Name", "Movie ID", "Movie Title", "Gender", "Position"])
```

Table shape
```python
print(tabMovieCharacters.shape)
```

Table columns
```python
print(tabMovieCharacters.columns)
```

Table information
```python
print(tabMovieCharacters.info())
```

__Movie Lines__

```python
tabMovieLines = pd.read_csv("Data/MovieLines.csv", sep="|", encoding="ISO-8859-1", header=None, names=["Line ID", "Character ID", "Movie ID", "Character Name", "Dialogue"])
```

Table shape
```python
print(tabMovieLines.shape)
```

Table columns
```python
print(tabMovieLines.columns)
```

Table information
```python
print(tabMovieLines.info())
```

__Movie Conversations__

```python
tabMovieConversations = pd.read_csv("Data/MovieConversations.csv", encoding="ISO-8859-1", sep="|", header=None, names=["ID First", "ID Second", "Movie ID", "Conversation"])
```

Table shape
```python
print(tabMovieConversations.shape)
```

Table columns
```python
print(tabMovieConversations.columns)
```

Table information
```python
print(tabMovieConversations.info())
```

__Movie Raw Script URLs__

```python
tabMovieRawScriptURLs = pd.read_csv("Data/MovieRawScriptURLs.csv", encoding="ISO-8859-1", sep="|", header=None, names=["Movie ID", "Movie Title", "Raw Script URL"])
```

Table shape
```python
print(tabMovieConversations.shape)
```

### Data Cleaning (Post-load)

* _tabMovieTitles_ has certain years that are appended with '/I' characters at the end. These have been trimmed and the year column has been converted to date-time format

Trimming trailing characters
```python
tabMovieTitles['Year'] = tabMovieTitles['Year'].map(lambda x: x.rstrip('/I'))
```

Converting column to date-time format
```python
tabMovieTitles['Year'] = pd.to_datetime(tabMovieTitles['Year'], format='%Y')
```

* _tabMovieCharacters_ has multiple formats of expressing males ('M' and 'm') and females ('F', 'f')  as shown below. We will reconcile these values to only 'm' for males and 'f' for females.

```python
print(tabMovieCharacters.Gender.value_counts())

tabMovieCharacters.loc[tabMovieCharacters['Gender'] == 'M', 'Gender'] = 'm'

tabMovieCharacters.loc[tabMovieCharacters['Gender'] == 'F', 'Gender'] = 'f'

print(tabMovieCharacters.Gender.value_counts())
```

### Merging the Dataset

Merging the datasets _tabMovieTitles_, _tabMovieCharacters_, _tabMovieLines_, and _tabMovieRawScriptURLs_ for easier processing. We're using _tabMovieLines_ as the primary table because it has the most granular data and performing 'left join' on it with the other tables. The table _tabMovieConversations_ will be kept separate as it depicts a different type of information.

```python
tabMovieLinesFull = pd.merge(tabMovieLines, tabMovieCharacters[['Character ID', 'Character Name', 'Gender', 'Position']], on='Character ID')

tabMovieLinesFull = tabMovieLinesFull.drop(['Character Name_x'], axis=1)

tabMovieLinesFull = tabMovieLinesFull.rename(columns = {'Character Name_y': 'Character Name'})

tabMovieLinesFull = pd.merge(tabMovieLinesFull, tabMovieTitles, on='Movie ID')

tabMovieLinesFull = pd.merge(tabMovieLinesFull, tabMovieRawScriptURLs[['Movie ID', 'Raw Script URL']], on='Movie ID')

tabMovieLinesFull = tabMovieLinesFull.set_index('Line ID')

print(tabMovieLinesFull.shape)
```
The merged dataset _tabMovieLinesFull_ has 303,249 records and 12 attributes and 'Line ID' column as the primary index.

#### Grouping by Gender

We will first calculate quantitative properties of individual dialogues for our analysis. Then, we will group the data by gender to discover patterns.

Calculating quantitative properties like length and total words:
```python
tabMovieLinesFull['Release Year'] = pd.DatetimeIndex(tabMovieLinesFull['Year']).year

tabMovieLinesFull['Dialogue Length'] = tabMovieLinesFull['Dialogue'].str.len()

tabMovieLinesFull['Dialogue Words'] = tabMovieLinesFull['Dialogue'].str.split().str.len()
```

Grouping into gender groups:
```python
tabGenderGroups = tabMovieLinesFull[tabMovieLinesFull.Gender != '?'].groupby('Gender').agg({
    'Character ID':['nunique'],
    'Dialogue Length':['sum', 'mean'],
    'Dialogue Words':['sum', 'mean']
     })

tabGenderGroups.reset_index(inplace=True)

tabGenderGroups.columns = ['Gender', 'Total Characters', 'Cumulative Sentence Length', 'Avg Sentence Length', 'Cumulative Words', 'Avg Words Per Sentence']
```

#### Visually Exploring the Data

The following charts are visual representations of the data that is available to us after excluding rows without clearly specified gender.

###### Yearly dialogues available in our dataset:
```python
YearlyDialogues = tabMovieLinesFull.groupby('Release Year').agg({
    'Dialogue': ['count']
    })

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
```

<img src="Assets/Visualizations/Yearly Dialogues.png"
     alt="ERD"
     style="width: 400px; height: 300px;" />

###### Yearly movies available in our dataset:
```python
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
```

<img src="Assets/Visualizations/Yearly Movies.png"
    alt="ERD"
    style="width: 400px; height: 300px;" />

###### Total genders available in our dataset:
```python
plt.bar(tabGenderGroups['Gender'], tabGenderGroups['Total Characters'], align='center', width=0.4)
locations, labels = xticks()
plt.xlabel('Gender')
plt.ylabel('Total Characters')
plt.title('Character Genders')
plt.xticks(locations, ['Female', 'Males'])
plt.show()
```

<img src="Assets/Visualizations/Character Genders.png"
    alt="ERD"
    style="width: 400px; height: 300px;" />

#### Visualizing Gender Differences

###### Cumulative sentence length:
```python
plt.bar(tabGenderGroups['Gender'], tabGenderGroups['Cumulative Sentence Length'], align='center', width=0.4)
locations, labels = xticks()
plt.xlabel('Gender')
plt.ylabel('Total Characters')
plt.title('Cumulative Sentence Length For Genders')
plt.xticks(locations, ['Female', 'Males'])
plt.show()
```

<img src="Assets/Visualizations/Cumulative Sentence Length.png"
    alt="ERD"
    style="width: 400px; height: 300px;" />

###### Average sentence length:
```python
plt.bar(tabGenderGroups['Gender'], tabGenderGroups['Avg Sentence Length'], align='center', width=0.4)
locations, labels = xticks()
plt.xlabel('Gender')
plt.ylabel('Total Characters')
plt.title('Average Sentence Length For Genders')
plt.xticks(locations, ['Female', 'Males'])
plt.show()
```

<img src="Assets/Visualizations/Avg Sentence Length.png"
    alt="ERD"
    style="width: 400px; height: 300px;" />

###### Cumulative words:
```python
plt.bar(tabGenderGroups['Gender'], tabGenderGroups['Cumulative Words'], align='center', width=0.4)
locations, labels = xticks()
plt.xlabel('Gender')
plt.ylabel('Total Words')
plt.title('Cumulative Words For Genders')
plt.xticks(locations, ['Female', 'Males'])
plt.show()
```

<img src="Assets/Visualizations/Cumulative Words.png"
    alt="ERD"
    style="width: 400px; height: 300px;" />

##### Average words per sentence:
```python
plt.bar(tabGenderGroups['Gender'], tabGenderGroups['Avg Words Per Sentence'], align='center', width=0.4)
locations, labels = xticks()
plt.xlabel('Gender')
plt.ylabel('Total Words')
plt.title('Average Words Per Sentence For Genders')
plt.xticks(locations, ['Female', 'Males'])
plt.show()
```

<img src="Assets/Visualizations/Avg Words Per Sentence.png"
    alt="ERD"
    style="width: 400px; height: 300px;" />

#### Sentiment Analyses

##### Tone

The Python library VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and rule-based sentiment analysis tool that is used to detect the semantic orientation of words (positive, negative, neutral, or compound). More information on this library can be found through this [link](https://github.com/cjhutto/vaderSentiment).

````python
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
````
