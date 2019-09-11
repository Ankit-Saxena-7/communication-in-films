## Discovering Patterns in Film Dialogues

A study on the quantitative and qualitative patterns in film dialogues across film genres, character gender, release year of the film, and so on.

## Affiliation

University: University of Pennsylvania  
Subject: Describing Your Data (COMM-783)  
Semester: Fall 2019

### Introduction

Effective dialogue between movie characters is one of the most important tools a filmmaker has to communicate the vision of their movie, move the plot forward, and engage the audience. Analyzing conversations between different movie characters can uncover the quantitative and qualitative differences between dialogues across different films and also uncover any forms of bias (like gender bias) that may exist in these conversations.

### The Data

The data set has been been extracted by the Cornell Movie - Dialogs Corpus that contains 220,579 conversational exchanges between 9,035 characters from 617 movies. In total, there are 304,713 dialogues taken from raw movie scripts. The entire data set is avaliable in Kaggle's website and can be accessed through this [link](https://www.kaggle.com/rajathmc/cornell-moviedialog-corpus).

The data has been systematically organized into five different tables in CSV format. Their contents are described below:

* _MovieTitles.csv_: Information about each movie title uniquely identified by the Movie ID column

* _MovieCharacters.csv_: All movie characters uniquely identified by the Character ID column

* _MovieLines.csv_: The actual text of each dialogue spoken uniquely identified by the Line ID column
  
* _MovieConversations.csv_: The structure of all conversations uniquely identified by the Character ID of the first character in the conversation, Character ID of the second character, and the Movie ID column

* _MovieRawScriptURL.csv_: The uniform resource locator (URL) of all the raw scripts
