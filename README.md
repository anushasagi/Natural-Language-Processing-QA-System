# Question - Answering System
A Q&A system which can answer various type of questions and provide answers by querying the three databases - Music, Movies and Geography. <br>
The input question is categorized into the respective category and an SQL statement is then framed my parsing the question in top-down approach. <br> 
This SQL statement is then used to query the respective database to obtain the answer. <br>

## Install Dependencies

* Core NLP Parser 
* NLTK 
* Wordnet
* SQLite

```
- from nltk.parse import CoreNLPParser (Runs on localhost:9000)
- pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')
- nltk.download('wordnet')
- from nltk.corpus import wordnet
- from nltk.tree import *
- import sqlite3
```

## How to Run the project
1. Run Code:
Run the code in command line as:
```
python <filename>.py "input.txt" "output.txt"
```

The output in the command line are some results from our implementation
The output of the project is written to a textfile named "output.txt"

2. WordNet:
This project uses WordNet for categorizing the questions.
Some important commands to run before executing:
```
nltk.download('wordnet')
```

3. Stanford/CoreNLP:
This project uses CoreNLPPaser integrated into nltk
```
from nltk.parse import CoreNLPParser
```
Runs on localhost:9000

4. Python Files:
Main Script 		              - ssagi2_mkandi3    <br>
Categorization Script         - NLP_Part1_Category.py <br>
WordNet Similarity Script     - NLP_Part1_Similarity_WordNet.py <br>
Movies Category Script	      - movies_Category.py  <br>
Music Category Script 	      - music_Category.py <br>
Geography Category Script     - geography_Category.py <br>
Database Script		            - Quering_On_Database.py  <br>
  
 ## Related Documents and Downloads
 -> For more details on how to install and CoreNLP API in NLTK, visit: https://github.com/nltk/nltk/wiki/Stanford-CoreNLP-API-in-NLTK <br>
 -> Run command to start CoreNLP running: 
 ```
 java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
-preload tokenize,ssplit,pos,lemma,ner,parse,depparse \
-status_port 9000 -port 9000 -timeout 15000 & 
```
 
