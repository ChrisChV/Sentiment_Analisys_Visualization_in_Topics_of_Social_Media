from preprocessing import *
from LDA import * 

doc_a = "Hola mundo este es el mensaje uno y dos por dos. Queremos"
doc_b = "Adios mundo voy a ir a comer. Fin del mensaje 2."


doc_set = [doc_a, doc_b]
k_topics = 2
LDA_iterations = 100


dictionary, corpus = preprocessing(doc_set)
model = LDA(dictionary, corpus, k_topics, LDA_iterations)

print (model.print_topics(num_topics=k_topics, num_words=3))