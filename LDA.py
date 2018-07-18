from gensim.models.wrappers import LdaMallet
import os

def LDA(dictionary, corpus, k_topics, iterations):
	print("Iniciando LDA...")
	model = LdaMallet(os.path.dirname(os.path.abspath(__file__)) + '/mallet-2.0.8/bin/mallet', corpus=corpus, num_topics=k_topics, id2word=dictionary, iterations=iterations)
	return model


