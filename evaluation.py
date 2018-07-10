import math


def person(rusell_sents_vector):
	xMean = 0
	yMean = 0
	numerador = 0
	raiz1 = 0;
	raiz2 = 0;
	for point in rusell_sents_vector:
		xMean += point[0]
		yMean += point[1]
	xMean /= len(rusell_sents_vector)
	yMean /= len(rusell_sents_vector)
	for point in rusell_sents_vector:
		numerador += (point[0] - xMean) * (point[1] - yMean)
		raiz1 += math.pow(point[0] - xMean, 2)
		raiz2 += math.pow(point[1] - yMean, 2)
	return float(numerador) / float(math.sqrt(raiz1) * math.sqrt(raiz2))


def getTopic(tweet, topics, dictionaryWord, dictByTopic):
	valores = []
	suma = 0
	for i in range(0,len(topics)):
		suma = 0
		topic = topics[i]
		for word in tweet:
			suma += dictByTopic[i][word]
		valores.append(suma)

	#for topic in topics:
	#	dictByTopic = {}
	#	for i in range(0,len(topic)):
	#		dictByTopic[dictionaryWord[i]] = topic[i]
	#	suma = 0
		
	i_max = -1
	valor_max = -1	
	for i in range(0, len(valores)):
		if(i_max == -1 or valor_max < valores[i]):
			i_max = i
			valor_max = valores[i]
	return i_max