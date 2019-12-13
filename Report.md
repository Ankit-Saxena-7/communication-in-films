---
title: "Gender Differences in Film Conversations"
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
# Importing libraries
import pandas as pd
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

```python
# Importing libraries
from matplotlib import pyplot as plt
from matplotlib.pyplot import xticks
```

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

###### Finding yearly ratios of dialogues for men-women

```python
tabMovieLinesFull['Year'] = pd.DatetimeIndex(tabMovieLinesFull['Year']).year
tabYearlyGenderCount = tabMovieLinesFull.loc[tabMovieLinesFull.Gender != '?'].groupby(['Year' , 'Gender']).size()
tabYearlyGenderPercentages = tabYearlyGenderCount.groupby(level=0).apply(lambda x: x/float(x.sum()))
```

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

#### Sentiment Analysis

The Python library VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and rule-based sentiment analysis tool that is used to detect the semantic orientation of words (positive, negative, neutral, or compound). More information on this library can be found through this [link](https://github.com/cjhutto/vaderSentiment).

```python
# Importing libraries
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
```

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

#### Downloading the Tables

Downloading the tables to conduct further tests on MS Excel.

````python
tabYearlyGenderCount.to_csv('tabYearlyGenderCount.csv', sep=',', encoding='utf-8')
tabMovieConversations.to_csv('tabMovieConversations.csv', sep=',', encoding='utf-8')
tabGenderGroups.to_csv('tabGenderGroups.csv', sep=',', encoding='utf-8')
tabMovieLinesFull.to_csv('tabMovieLinesFull.csv', sep=',', encoding='utf-8')
tabYearlyGenderPercentages.to_csv('tabYearlyGenderPercentages.csv', sep=',', encoding='utf-8')
````

###### Finding conversation starters and finishers

Follow the steps in MS Excel to identify the gender of character starting and finishing conversations:

* Open the file _tabMovieConversations.csv_ in MS Excel
* Navigate to the column _Conversation_
* Use a combination of the Excel functions LEFT() and FIND() to find the first Line ID of each conversation, which represents the Line ID of the conversation starter. Name the resulting column Conversation Starter
* Use a combination of the Excel functions RIGHT() and FIND() to find the last Line ID of each conversation, which represents the Line ID of the conversation finisher. Name the resulting column Conversation Finisher.
* Use the VLOOKUP() function along with the columns Line ID and Gender columns in the downloaded Excel file _tabMovieLinesFull.csv_ to find out the genders of the conversation starters and finishers in the Excel sheet _tabMovieConversations.csv_. Name the resulting columns Starter Gender and Ender Gender.
* Use a similar process to find the genders of the two characters involved in the conversation (columns ID First and ID Second in _tabMovieConversations.csv_). Name the resulting columns First Gender and Second Gender.

#### Hypothesis Tests

Using the 't-test: Two-Sample Assuming Unequal Variances' feature in MS Excel's Data Analysis package, you can perform t-tests for the following hypotheses:

* Difference in average number of characters per dialogue for men and women: Using the columns Gender and Dialogue Length in _tabMovieLinesFull.csv_.
* Difference in average number of words per dialogue for men and women: Using the columns Gender and Dialogue Words in _tabMovieLinesFull.csv_.
* Difference in total number and average number per movie of conversation starters and finishers for men and women: Using the columns Starter Gender, Ender Gender, and Movie ID in _tabMovieConversations.csv_.
* Differences between number of conversations between men-men, men-women, and women-women: Using the columns First Gender and Second Gender in _tabMovieConversations.csv_.
* Differences in sentiment scores by VADER for men and women: Using the columns Sentiment Negative, Sentiment Neutral, Sentiment Positive, and Sentiment Compound in _tabMovieLinesFull.csv_.
