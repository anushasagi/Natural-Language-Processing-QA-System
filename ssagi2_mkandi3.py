from nltk.parse import CoreNLPParser

import sys
import pprint
from nltk.tree import *
import NLP_Part1_Category
import movies_Category
import music_Category
import geography_Category
import Quering_On_Database
import Quering_On_Database as QDB

# Lexical Parser
parser = CoreNLPParser(url='http://localhost:9000')
count = 0
final_result = []

input_filepath = sys.argv[1]
output_filepath = sys.argv[2]

open(output_filepath, "w").close()

f2 = open(output_filepath, "a")


def print_result (result):
    final_result = []
    f2.write("Answer:")
    f2.write("\n")
    for item in result:
        final_result.append("%s" % item)
        for f in final_result:
            if len(str(f)) > 1:
                f2.write(f)
            elif int(f) > 0:
                f2.write ("Yes")
            elif int(f) == 0:
                f2.write("No")
            else:
                f2.write("I don't Know")
        final_result = []
    f2.write("\n\n")
    
def movies_music(question):
    category = ""
    movie_names = []
    movnames = QDB.get_movie_names()
    for mn in movnames:
        movie_names.append(" %s" % mn)
    for i in movie_names:
        if i.lower() in question.lower():
            category = "Movies"

    album_names = list()
    track_names = list()
    albnames = QDB.get_album_names()
    for an in albnames:
        album_names.append(" %s" % an)
    for i in album_names:
        if i.lower() in question.lower():
            category = "Music"

    trknames = QDB.get_track_names()
    for tn in trknames:
        track_names.append(" %s" % tn)
    for i in track_names:
        if i.lower() in question.lower():
            category = "Music"

    return category


with open(input_filepath, "r") as f1:
    for line in f1:
    	question = line.strip()
    	if  question != "":
            count = count + 1
            c = str(count)

            l1 = "Question "+c+": "+question
            l2 = "Parse Tree:"
            l3 = list(parser.raw_parse(question))
            tree1 = parser.raw_parse(question)

            print (l1)
            print (l2)
            print (l3)

            f2.write (l1)
            f2.write ("\n")

            category = movies_music(question)
            if category == "":
                final_category = NLP_Part1_Category.categorize(question)
            else:
                final_category = category
            f2.write ("Category: "+final_category)
            f2.write ("\n")

            f2.write (l2)
            f2.write ("\n")
            for item in l3:
                f2.write("%s\n" % item)

            if final_category == "Movies":
                print ("Movies category")
                sql_statement = movies_Category.movies_category(question)
                f2.write("SQL statement:")
                f2.write("\n")
                f2.write(sql_statement)
                f2.write("\n")
                result = Quering_On_Database.movie_database(sql_statement)
                print_result(result)
                

            if final_category == "Music":
                print ("Music category")
                sql_statement = music_Category.music_category(question)
                f2.write("SQL statement:")
                f2.write("\n")
                f2.write(sql_statement)
                f2.write("\n")
                result = Quering_On_Database.music_database(sql_statement)
                print_result(result)

            if final_category == "Geography":
                print ("Geography category")
                sql_statement = geography_Category.geography_category(question)
                f2.write("SQL statement:")
                f2.write("\n")
                f2.write(sql_statement)
                f2.write("\n")
                result = Quering_On_Database.geography_database(sql_statement)
                print_result(result)




f1.close()
f2.close()




