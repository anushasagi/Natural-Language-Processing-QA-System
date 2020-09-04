# Question - Answering System
A Q&A system which can answer various type of questions and provide answers by querying the three databases - Music, Movies and Geography.
The input question is categorized into the respective category and an SQL statement is then framed my parsing the question in top-down approach. 
This SQL statement is then used to query the respective database to obtain the answer.

## Install Dependencies

* Core NLP Parser 
* NLTK 
* Wordnet
* SQLite

- nltk.download('wordnet')
- from nltk.parse import CoreNLPParser (Runs on localhost:9000)

## How to Run the project
1. Run Code:
Run the code in command line as:
python <filename>.py "input.txt" "output.txt"

The output in the command line are some results from our implementation
The output of the project is written to a textfile named "output.txt"

2. WordNet:
This project uses WordNet for categorizing the questions.
Some important commands to run before executing: nltk.download('wordnet')

3. Stanford/CoreNLP:
This project uses CoreNLPPaser integrated into nltk
from nltk.parse import CoreNLPParser
Runs on localhost:9000

4. Python Files:
Main Script 		              - ssagi2_mkandi3
Categorization Script         - NLP_Part1_Category.py
WordNet Similarity Script     - NLP_Part1_Similarity_WordNet.py
Movies Category Script	      - movies_Category.py
Music Category Script 	      - music_Category.py
Geography Category Script     - geography_Category.py
Database Script		            - Quering_On_Database.py
  
 ## Related Documents and Downloads
 -> For more details on how to install and CoreNLP API in NLTK, visit: https://github.com/nltk/nltk/wiki/Stanford-CoreNLP-API-in-NLTK
 -> Run command to start CoreNLP running: java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
-preload tokenize,ssplit,pos,lemma,ner,parse,depparse \
-status_port 9000 -port 9000 -timeout 15000 & 
 
