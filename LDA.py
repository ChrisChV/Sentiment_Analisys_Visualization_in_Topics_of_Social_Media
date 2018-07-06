from gensim.models.wrappers import LdaMallet

def LDA(dictionary, corpus, k_topics, iterations):
	print("Iniciando LDA...")
	model = LdaMallet('./mallet-2.0.8/bin/mallet', corpus=corpus, num_topics=k_topics, id2word=dictionary, iterations=iterations)
	return model


