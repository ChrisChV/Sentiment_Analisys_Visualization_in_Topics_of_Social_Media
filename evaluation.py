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