from nltk.parse import CoreNLPParser
from nltk.tree import *
import pprint
import xml.etree.ElementTree as ET
import Quering_On_Database as QDB


def movies_category (question):
    parser = CoreNLPParser(url='http://localhost:9000')
    ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
    quest = question
    l3 = list(parser.raw_parse(quest))
    #pretty print parser
    Tree.fromstring(str(l3[0])).pretty_print()
    print("********************")

    selectQ = ""
    fromQ = []
    tempfromQ =[]
    tempwhereQ = []
    whereQ = []
    query_variables = []
    person_list = []
    country_list = []
    date_list = []
    nationality_list = []
    title_list = []
    movie_names = []
    movie_name = ""

    fromQ.append(" from")
    whereQ.append(" where")


    ptree = ParentedTree.fromstring(str(l3[0]))
    rules = ptree.productions()
    print (rules)

    for i in rules:
        l1 = "Rule: "+str(i)
        print (l1)

    l4 = list(ner_tagger.tag((quest.split())))
    print (l4)

    for word, category in l4:
        if category == 'PERSON':
            person_list.append(word)
        if category == 'COUNTRY':
            country_list.append(word)
        if category == 'DATE':
            date_list.append(word)
        if category == 'NATIONALITY':
            nationality_list.append(word)
        if category == 'TITLE':
            title_list.append(word)       

    print ("Person List:")
    print (person_list)
    print ("Country List:")
    print (country_list)
    print ("Date List:")
    print (date_list)
    print ("Nationality List:")
    print (nationality_list)
    print ("Title List:")
    print (title_list)


    movnames = QDB.get_movie_names()
    for mn in movnames:
        movie_names.append(" %s" % mn)
    for i in movie_names:
        if i.lower() in quest.lower():
            movie_name = i
    print("Movie Name: "+movie_name)
    movie_name = movie_name.strip()

    print("********************************")
    print (type(rules))

    str_rules = str(rules) 

    if 'ROOT -> SBARQ' in str_rules:
        #WH Questions
        print("WH Questions")
        selectQ = ""

        for i in rules:
            if 'NNP ->' in str(i):
                print ("Query variables")
                qvar = str(i).split('NNP ->',1)[1]
                qvar = qvar.strip()
                qvar = qvar[1:-1]
                query_variables.append(qvar)

        for i in rules:
            if 'WP ->' in str(i):
                print ("WP")
                x1 = str(i).split('WP ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1.lower() == 'who':
                    selectQ = "select P.name"
                    fromQ.append(" Person P")
            if 'WDT ->' in str(i):
                print ("WDT")
                x1 = str(i).split('WDT ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1.lower() == 'which' and 'movie' in quest:
                    selectQ = "select M.name"
                    fromQ.append(" Movie M")
                elif x1.lower() == 'which':
                    selectQ = "select P.name"
                    fromQ.append(" Person P")
            if 'WRB ->' in str(i):
                print ("WRB")
                x1 = str(i).split('WRB ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1.lower() == 'when':
                    selectQ = "select O.year"
                    fromQ.append(" Oscar O")
                    for qv in query_variables:
                        whereQ.append(" P.name like '%"+qv+"%'")
            if 'VBD ->' in str(i):
                print ("VBD")
                x1 = str(i).split('VBD ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1 == 'directed' and 'movie' not in quest:
                    fromQ.append(" INNER JOIN Director D ON P.id = D.director_id")
                    fromQ.append(" INNER JOIN MOVIE M ON D.movie_id = M.id")
                    '''for qv in query_variables:
                        if qv not in person_list and qv not in country_list and qv not in date_list:'''
                    whereQ.append(" M.name like '%"+movie_name+"%'")
                if x1 == 'directed' and query_variables == []:
                    fromQ.append(" INNER JOIN Director D ON P.id = D.director_id")
                    fromQ.append(" INNER JOIN OSCAR O ON D.movie_id = O.movie_id")
                if x1 == "won" and 'movie' in quest:
                    fromQ.append(" INNER JOIN Oscar O ON M.id = O.movie_id")   
                elif x1 == "won":
                    fromQ.append(" INNER JOIN Oscar O ON P.id = O.person_id")
            if 'VB ->' in str(i):
                print ("VB")
                x1 = str(i).split('VB ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1 == "win":
                    fromQ.append(" INNER JOIN Person P ON O.person_id = P.id")
            if 'NN ->' in str(i):
                print ("NN")
                x1 = str(i).split('NN ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if "actor" in x1.lower():
                    Otype = "BEST-ACTOR"
                    whereQ.append(" O.type like '%"+Otype+"%'")
                elif "actress" in x1.lower():
                    Otype = "BEST-ACTRESS"
                    whereQ.append(" O.type like '%"+Otype+"%'")
                elif "movie" in x1.lower():
                    Otype = "BEST-PICTURE"
                    whereQ.append(" O.type like '%"+Otype+"%'")
                elif "director" in x1.lower():
                    Otype = "BEST-DIRECTOR"
                    whereQ.append(" O.type like '%"+Otype+"%'")
            if 'CD ->' in str(i):
                print ("CD")
                x1 = str(i).split('CD ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1 in date_list:
                    whereQ.append(" O.year like '%"+x1+"%'")
            if 'JJ ->' in str(i):
                print ("JJ Nationality")
                x1 = str(i).split('JJ ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1 in nationality_list:
                    '''fromQ.append(" Person P")'''
                    if x1.lower() == "french":
                        nat_word = "France"
                    elif x1.lower() == "american":
                        nat_word = "USA"
                    elif x1.lower() == "italian":
                        nat_word = "Italy"
                    elif x1.lower() == "british":
                        nat_word = "UK"
                    elif x1.lower() == "german":
                        nat_word = "Germany"
                    whereQ.append(" P.pob like '%"+nat_word+"%'")

                


    elif 'ROOT -> S' in str_rules:
        #Yes/No Questions
        print("Yes/No Questions")
        selectQ = "select count(*)"

        for i in rules:
            if 'NNP ->' in str(i):
                print ("Query variables")
                qvar = str(i).split('NNP ->',1)[1]
                qvar = qvar.strip()
                qvar = qvar[1:-1]
                query_variables.append(qvar)
        
        for i in rules:
            if 'NNP ->' in str(i):
                print ("NNP")
                x1 = str(i).split('NNP ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1 in person_list:
                    fromQ.append(" Person P")
                    whereQ.append(" P.name like '%"+x1+"%'")
                elif x1 in country_list:
                    whereQ.append(" P.pob like '%"+x1+"%'")
                elif date_list != []:
                    fromQ.append(" Movie M")
                    fromQ.append(" INNER JOIN Oscar O ON M.id = O.movie_id")
                    whereQ.append(" M.name like '%"+movie_name+"%'")
            if 'NN ->' in str(i):
                print ("NN")
                x1 = str(i).split('NN ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if "actor" in x1.lower() and "Is" not in quest:
                    Otype = "BEST-ACTOR"
                    whereQ.append(" O.type like '%"+Otype+"%'")
                elif "actress" in x1.lower() and "Is" not in quest:
                    Otype = "BEST-ACTRESS"
                    whereQ.append(" O.type like '%"+Otype+"%'")
                elif "movie" in x1.lower() and "Is" not in quest:
                    Otype = "BEST-PICTURE"
                    whereQ.append(" O.type like '%"+Otype+"%'")
                elif "director" in x1.lower() and "Is" not in quest:
                    Otype = "BEST-DIRECTOR"
                    whereQ.append(" O.type like '%"+Otype+"%'")
            if 'CD ->' in str(i):
                print ("CD")
                x1 = str(i).split('CD ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1 in date_list:
                    whereQ.append(" O.year like '%"+x1+"%'")
            if 'IN ->' in str(i):
                print ("IN")
                x1 = str(i).split('IN ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1 == "by":
                    fromQ.append(" INNER JOIN Director D ON P.id = D.director_id")
                    fromQ.append(" INNER JOIN Movie M ON D.movie_id = M.id")
                    '''for qv in query_variables:
                        if qv not in person_list and qv not in country_list and qv not in date_list:'''
                    whereQ.append(" M.name like '%"+movie_name+"%'")
                if x1 == "with":
                    fromQ.append(" INNER JOIN Director D ON P.id = D.director_id")
                    fromQ.append(" INNER JOIN Oscar O ON D.movie_id = O.movie_id")
            if 'VB ->' in str(i):
                print ("VB")
                x1 = str(i).split('VB ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1 == "star":
                    fromQ.append(" INNER JOIN Actor A ON P.id = A.actor_id")
                    fromQ.append(" INNER JOIN Movie M ON A.movie_id = M.id")
                    '''for qv in query_variables:
                        if qv not in person_list and qv not in country_list and qv not in date_list:'''
                    whereQ.append(" M.name like '%"+movie_name+"%'")
                if x1 == "win":
                    fromQ.append(" INNER JOIN Oscar O ON P.id = O.person_id")
                if x1 == "direct":
                    fromQ.append(" INNER JOIN Director D ON P.id = D.director_id")
                    fromQ.append(" INNER JOIN Movie M ON D.movie_id = M.id")
                    '''for qv in query_variables:
                        if qv not in person_list and qv not in country_list and qv not in date_list:'''
                    whereQ.append(" M.name like '%"+movie_name+"%'")
            if 'VBZ ->' in str(i):
                print ("VBZ")
                x1 = str(i).split('VBZ ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1 == "Is" and 'director' in quest :
                    fromQ.append(" INNER JOIN Director D on P.id = D.director_id")
                elif x1 == "Is" and 'actor' in quest :
                    fromQ.append(" INNER JOIN Actor A on P.id = A.actor_id")
            if 'JJ ->' in str(i):
                print ("JJ Nationality")
                x1 = str(i).split('JJ ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1 in nationality_list:
                    fromQ.append(" Person P")
                    if x1.lower() == "french":
                        nat_word = "France"
                    elif x1.lower() == "american":
                        nat_word = "USA"
                    elif x1.lower() == "italian":
                        nat_word = "Italy"
                    elif x1.lower() == "british":
                        nat_word = "UK"
                    elif x1.lower() == "german":
                        nat_word = "Germany"
                    whereQ.append(" P.pob like '%"+nat_word+"%'")

    print ("Query variables: "+str(query_variables))
    print ("Select statement: "+str(selectQ))
    print ("From statement: "+str(fromQ))
    print ("Where statement: "+str(whereQ))
    print (str(selectQ) + str(fromQ) + str(whereQ))
    print("***************************************************")

    for f in fromQ:
        if 'from' in str(f):
            tempfromQ.append(str(f))
    for f in fromQ:
        if "INNER JOIN" not in f and "from" not in f:
            tempfromQ.append(str(f))
    for f in fromQ:
        if "INNER JOIN" in f:
            tempfromQ.append(str(f))
        '''elif " from" in tempfromQ[len(tempfromQ)-1] and f != " from":
            tempfromQ.append(str(f))'''

    print ("From statement: "+str(tempfromQ))

    for w in whereQ:
        if 'where' in str(w):
            tempwhereQ.append(w)
    for w in whereQ:
        if "like" in tempwhereQ[len(tempwhereQ)-1]:
            tempwhereQ.append(" and")
            tempwhereQ.append(str(w))
        elif " where" in tempwhereQ[len(tempwhereQ)-1] and w != " where":
            tempwhereQ.append(str(w))

    print ("Where statement: "+str(tempwhereQ))

    print ("*************************************************")
    #building query
    from_statement = ""
    where_statement = ""
    final_query = ""
    for each_from in tempfromQ:
        from_statement = from_statement + str(each_from)
    for each_where in tempwhereQ:
        where_statement = where_statement + str(each_where)

    final_query = final_query + str(selectQ) + str(from_statement) + str(where_statement)
    print (final_query)
    return final_query
