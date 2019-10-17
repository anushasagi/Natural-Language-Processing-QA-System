from nltk.parse import CoreNLPParser
from nltk.tree import *
import pprint
import xml.etree.ElementTree as ET
import Quering_On_Database as QDB

def music_category (question):
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
    state_list = []
    album_names = list()
    track_names = list()
    album_name = ""
    track_name = ""

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
        if category == 'STATE_OR_PROVINCE':
            state_list.append(word)


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
    print ("State List:")
    print (state_list)

    albnames = QDB.get_album_names()
    for an in albnames:
        album_names.append(" %s" % an)
    for i in album_names:
        if i.lower() in quest.lower():
            album_name = i
    print("Album Name: "+album_name)
    album_name = album_name.strip()

    trknames = QDB.get_track_names()
    for tn in trknames:
        track_names.append(" %s" % tn)
    for i in track_names:
        if i.lower() in quest.lower():
            track_name = i
    print("Track Name: "+track_name)
    track_name = track_name.strip()



    print("********************************")
    print (type(rules))

    str_rules = str(rules) 


    #*********************************************

    if 'ROOT -> SBARQ' in str_rules:
        #Wh Questions
        print("Wh Questions")
        selectQ = ""

        for i in rules:
            if 'NNP ->' in str(i):
                print ("Query variables")
                qvar = str(i).split('NNP ->',1)[1]
                qvar = qvar.strip()
                qvar = qvar[1:-1]
                query_variables.append(qvar)

        for i in rules:
            if 'WDT ->' in str(i):
                print ("WDT")
                x1 = str(i).split('WDT ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1.lower() == 'which' and "artist" in title_list:
                    selectQ = "select A.name"
                    fromQ.append(" Artist A")
                if x1.lower() == 'which' and "album" in quest:
                    selectQ = "select AL.name"
                    fromQ.append(" Album AL")
            if 'WRB ->' in str(i):
                print ("WRB")
                x1 = str(i).split('WRB ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1.lower() == 'where':
                    selectQ = "select A.placeOfBith"
                if x1.lower() == 'when':
                    selectQ = "select A.dateOfBirth"

            if 'VBZ ->' in str(i):
                print ("VBZ")
                x1 = str(i).split('VBZ ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1 == "sings":
                    fromQ.append(" INNER JOIN Album AL ON A.id = AL.artsitID")
                    fromQ.append(" INNER JOIN Track T ON AL.albumID = T.albumID")
                    whereQ.append(" T.name like '%"+track_name+"%'")
            if 'IN ->' in str(i):
                print ("IN")
                x1 = str(i).split('IN ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1 == "by" and person_list != []:
                    fromQ.append(" INNER JOIN Artist A ON AL.artsitID = A.id")
                    for p in person_list:
                        whereQ.append(" A.name like '%"+p+"%'")
            if 'VBN ->' in str(i):
                print ("VBN")
                x1 = str(i).split('VBN ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1 == "released":
                    for d in date_list:
                        whereQ.append(" AL.releaseDate like '%"+d+"%'")
                if x1 == "born":
                    fromQ.append(" Artist A")
                    for qv in query_variables:
                        whereQ.append(" A.name like '%"+qv+"%'")



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
                    fromQ.append(" Artist A")
                    whereQ.append(" A.name like '%"+x1+"%'")
            if 'NN ->' in str(i):
                print ("NN")
                x1 = str(i).split('NN ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1 == "album":
                    fromQ.append(" Album AL")
                    whereQ.append(" AL.name like '%"+album_name+"%'")
                if x1 == "track":
                    fromQ.append(" INNER JOIN Track T ON AL.albumID = T.albumID")
                    whereQ.append(" T.name like '%"+track_name+"%'")

            if 'VB ->' in str(i):
                print ("VB")
                x1 = str(i).split('VB ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1 == "sing":
                    fromQ.append(" INNER JOIN Album AL ON A.id = AL.artsitID")
                    fromQ.append(" INNER JOIN Track T ON AL.albumID = T.albumID")
                    whereQ.append(" T.name like '%"+track_name+"%'")
            if 'VBN ->' in str(i):
                print ("VBN")
                x1 = str(i).split('VBN ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1 == "born":
                    for qv in query_variables:
                        if qv not in person_list and qv in country_list or qv in state_list:
                            #Contry/State in Artist table
                            whereQ.append(" A.placeOfBith like '%"+qv+"%'")




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