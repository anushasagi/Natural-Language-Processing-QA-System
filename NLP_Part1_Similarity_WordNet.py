import nltk
#nltk.download('wordnet')
from nltk.corpus import wordnet as wn

def similarity_main (word, postype):
	list1_noun = ['Geography.n.01', 'Location.n.01', 'Place.n.01', 'capital.n.01']
	list1_verb = ['lie.v.01']
	list2_noun = ['Movie.n.01', 'Actor.n.01', 'actress.n.01', 'Film.n.01', 'Oscar.n.01', 'director.n.01']
	list2_verb = ['Act.v.01','star.v.01', 'direct.v.01']
	list3_noun = ['Music.n.01', 'singer.n.01', 'Album.n.01', 'track.n.01', 'artist.n.01']
	list3_verb = ['sing.v.01']

	category1_count = 0
	category2_count = 0
	category3_count = 0

	if postype == "NOUN":
		p = wn.NOUN
		list1 = list1_noun
		list2 = list2_noun
		list3 = list3_noun
	elif postype == "VERB":
		p = wn.VERB
		list1 = list1_verb
		list2 = list2_verb
		list3 = list3_verb
	sent_word = wn.synsets(word, pos = p)
	print (sent_word)

	templist = list1
	category_count = category1_count 
	category1_count = check_similarity(templist, sent_word, category1_count)
	print ("Geography: "+str(category1_count))
	print("**************************************************************************")

	templist = list2
	category_count = category2_count 
	category2_count = check_similarity(templist, sent_word, category2_count)
	print ("Movies: "+str(category2_count))
	print("**************************************************************************")

	templist = list3
	category_count = category3_count 
	category3_count = check_similarity(templist, sent_word, category3_count)
	print ("Music: "+str(category3_count))
	print("**************************************************************************")

	if category1_count > category2_count and category1_count > category3_count:
		return ("Geography")
	if category2_count > category1_count and category2_count > category3_count:
		return ("Movies")
	if category3_count > category1_count and category3_count > category2_count:
		return ("Music")



def check_similarity(templist, sent_word, category_count):
	count = 0
	if len(sent_word) != 0:
		for word in templist:
			category = wn.synset(word)
			#category = word
			print (category)
			result = sent_word[0].path_similarity(category)
			if result is None:
				result = 0
			print (result)
			category_count = category_count + result
			count = count + 1
		print (category_count)
		print (count)
		return (category_count/count)
	else:
		return 0
	





