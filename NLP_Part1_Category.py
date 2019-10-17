from nltk.parse import CoreNLPParser
import NLP_Part1_Similarity_WordNet

pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')

def find_category(poslist, postype):
	category_list = []
	for word in poslist:
		category = NLP_Part1_Similarity_WordNet.similarity_main(word, postype)
		category_list.append(category)
	return (category_list)




def categorize(line):
	line = line.strip()
	if  line != "":
		noun_category = ""
		propernoun_category = ""
		verb_category = ""
		nounlist = []
		propernounlist = []
		verblist = []
		adjectlist = []
		adverblist = []
		tags = list(pos_tagger.tag(line.split()))
		print (tags)
		for word, taggy in tags:
			if taggy == 'NN' or taggy =='NNS':
				nounlist.append(word)
			if taggy == 'NNP' or taggy == 'NNPS':
				propernounlist.append(word)
			if taggy == 'VB' or taggy == 'VBD' or taggy == 'VBG' or taggy == 'VBN' or taggy == 'VBP' or taggy =='VBZ':
				verblist.append(word)
			if taggy == 'JJ' or taggy == 'JJR' or taggy == 'JJS':
				adjectlist.append(word)
			if taggy == 'RB' or taggy == 'RBR' or taggy == 'RBS' or taggy == 'WRB':
				adverblist.append(word)


		print ("Common Nouns:",nounlist)
		print ("Proper Nouns:",propernounlist)
		print ("Verbs:",verblist)
		print ("Adverbs:", adverblist)
		print ("Adjectives:", adjectlist)
			

		if len(nounlist) != 0:
			poslist = nounlist
			postype = "NOUN"
			noun_category = find_category(poslist, postype)
			geography_count = noun_category.count("Geography")
			movies_count = noun_category.count("Movies")
			music_count = noun_category.count("Music")
			if movies_count > 0:
				noun_category = "Movies"
			elif music_count > 0:
				noun_category = "Music"
			else:
				noun_category = "Geography"
				
		if len(propernounlist) != 0:
			poslist = propernounlist
			postype = "NOUN"
			propernoun_category = find_category(poslist, postype)
			geography_count = propernoun_category.count("Geography")
			movies_count = propernoun_category.count("Movies")
			music_count = propernoun_category.count("Music")
			if movies_count > 0:
				propernoun_category = "Movies"
			elif music_count > 0:
				propernoun_category = "Music"
			else:
				propernoun_category = "Geography"
				
					
		if len(verblist) != 0:
			poslist = verblist
			postype = "VERB"
			verb_category = find_category(poslist, postype)
			geography_count = verb_category.count("Geography")
			movies_count = verb_category.count("Movies")
			music_count = verb_category.count("Music")
			if movies_count > 0:
				verb_category = "Movies"
			elif music_count > 0:
				verb_category = "Music"
			else:
				verb_category = "Geography"

				
		#f2.write ("Question: "+line)
		#f2.write ("\n")
		noun_category = str(noun_category)
		propernoun_category = str(propernoun_category)
		verb_category = str(verb_category)

		if noun_category != "":
			final_category = noun_category
		elif verb_category != "":
			final_category = verb_category
		else:
			final_category = propernoun_category

		del nounlist, verblist, propernounlist, adjectlist, adverblist

		return final_category
			




			


			
