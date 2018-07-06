from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from gensim import corpora, models
from nltk.stem.snowball import SnowballStemmer
import Stemmer

def preprocessing(doc_set):
	print("Iniciando preprocesamiento...")
	tokenizer = RegexpTokenizer(r'\w+')
	es_stop = get_stop_words('es')
	#stemmer = Stemmer.Stemmer('spanish')
	stemmer = SnowballStemmer('spanish')

	out_set = []

	for doc in doc_set:
		raw = doc.lower()
		tokens = tokenizer.tokenize(raw)

		stooped_tokens = [i for i in tokens if not i in es_stop]

		#stemmer_words = stemmer.stemWords(stooped_tokens)

		stemmer_words = []
		for word in stooped_tokens:
			stemmer_words.append(stemmer.stem(word))
		
		out_set.append(stemmer_words)


	dictionary = corpora.Dictionary(out_set) #diccionario con las palabras enlazadas a una id
	corpus = [dictionary.doc2bow(doc) for doc in out_set]
	#print(corpus[0]) #imprime la bolsa de palabras, son tuplas de la forma (termID, termfrecuency) en el documento 0
	#print(corpus[1]) 

	print("Done")

	return dictionary , corpus





