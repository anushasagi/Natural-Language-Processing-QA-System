from nltk.parse import CoreNLPParser
from nltk.tree import *
import pprint
import xml.etree.ElementTree as ET
import Quering_On_Database as QDB

def geography_category (question):
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
    city_list = []
    country_list = []
    location_list = []


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
        if category == 'CITY':
            city_list.append(word)
        if category == 'COUNTRY':
            country_list.append(word)
        if category == 'LOCATION':
            location_list.append(word)



    print ("City List:")
    print (city_list)
    print ("Country List:")
    print (country_list)
    print ("Location List:")
    print (location_list)


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
            if 'WP ->' in str(i):
                    print ("WP")
                    x1 = str(i).split('WP ->',1)[1]
                    x1 = x1.strip()
                    x1 = x1[1:-1]
                    if x1.lower() == 'what' and city_list == [] and country_list != []:
                        selectQ = "select CI.name"
                        fromQ.append(" CITIES CI")
                        fromQ.append(" INNER JOIN Capitals CA on CI.Id = CA.CityId")
            if 'WRB ->' in str(i):
                    print ("WRB")
                    x1 = str(i).split('WRB ->',1)[1]
                    x1 = x1.strip()
                    x1 = x1[1:-1]
                    if x1.lower() == 'where' and city_list != []:
                        for city in city_list:
                            selectQ = "select CY.name"
                            fromQ.append(" Countries CY")
                            fromQ.append(" INNER JOIN Capitals CA on CY.Id = CA.CountryId")
                            fromQ.append(" INNER JOIN Cities CI on CA.CityId = CI.Id")
                            whereQ.append(" CI.name like '%"+city+"%'")
                    if x1.lower() == 'where' and country_list != []:
                        for country in country_list:
                            selectQ = "select CO.continent"
                            fromQ.append(" Continents CO")
                            fromQ.append(" INNER JOIN CountryContinents CC on CO.Id = CC.ContinentId")
                            fromQ.append(" INNER JOIN Countries CY on CC.CountryId = CY.Id")
                            whereQ.append(" CY.name like '%"+country+"%'")
            if 'NN ->' in str(i):
                print ("NN")
                x1 = str(i).split('NN ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1 == "capital":
                    if country_list != []:
                        for country in country_list:
                            fromQ.append(" INNER JOIN Countries CY on CA.CountryId = CY.Id")
                            whereQ.append(" CY.name like '%"+country+"%'")
        


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
            if 'NN ->' in str(i):
                print ("NN")
                x1 = str(i).split('NN ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1 == "capital":
                    if city_list != []:
                        for city in city_list:
                            fromQ.append(" CITIES CI")
                            fromQ.append(" INNER JOIN Capitals CA on CI.Id = CA.CityId")
                            whereQ.append(" CI.name like '%"+city+"%'")
                    if country_list != []:
                        for country in country_list:
                            fromQ.append(" INNER JOIN Countries CY on CA.CountryId = CY.Id")
                            whereQ.append(" CY.name like '%"+country+"%'")
            if 'IN ->' in str(i):
                print ("IN")
                x1 = str(i).split('IN ->',1)[1]
                x1 = x1.strip()
                x1 = x1[1:-1]
                if x1 == "in":
                    if country_list != [] and location_list != []:
                        for country in country_list:
                            fromQ.append(" Countries CY")
                            fromQ.append(" INNER JOIN CountryContinents CC on CY.Id = CC.CountryId")
                            whereQ.append(" CY.name like '%"+country+"%'")
                        for continent in location_list:
                            fromQ.append(" INNER JOIN Continents CO on CC.ContinentId = CO.Id")
                            whereQ.append(" CO.continent like '%"+continent+"%'")
                    if city_list != [] and country_list != []:
                            for city in city_list: 
                                fromQ.append(" CITIES CI")
                                fromQ.append(" INNER JOIN Capitals CA on CI.Id = CA.cityId")
                                whereQ.append(" CI.name like '%"+city+"%'")
                            for country in country_list:
                                fromQ.append(" INNER JOIN Countries CY on CA.CountryId = CY.Id")
                                whereQ.append(" CY.name like '%"+country+"%'")
            


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