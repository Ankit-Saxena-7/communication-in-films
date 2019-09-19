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

### Coding standards

* Entities like variables and functions have been named using camel case convention
* Local variables have been prefixed using 'v'
* Global variables have been prefixed using 'g'
* Tables have been prefixed using 'tab'

### Importing Packages
The following packages will need to be imported for the analysis:

```python
import pandas as pd
```

### Importing the Data

Run the following scripts to import the data from your repository and check the dimensions of each table to makes sure the complete set has been loaded.

__Movie Titles__

```python
tabMovieTitles = pd.read_csv(file="Data/MovieTitles.csv", sep="|")
```


```python
print(tabMovieTitles.shape)
```

__Movie Characters__

```python
tabMovieCharacters = pd.read_csv(file="Data/MovieCharacters.csv", sep="|")
```


```python
print(tabMovieCharacters.shape)
```

__Movie Lines__

```python
tabMovieLines = pd.read_csv(file="Data/MovieLines.csv", sep="|")
```


```python
print(tabMovieLines.shape)
```

__Movie Conversations__

```python
tabMovieConversations = pd.read_csv(file="Data/MovieConversations.csv", sep="|")
```


```python
print(tabMovieConversations.shape)
```

__Movie Raw Script URLs__

```python
tabMovieRawScriptURLs = pd.read_csv(file="Data/MovieRawScriptURLs.csv", sep="|")
```


```python
print(tabMovieRawScriptURLs.shape)
```
