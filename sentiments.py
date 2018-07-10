from enum import Enum
import math

class Sentiments(Enum):
	FELIZ = 0
	EXALTADO = 1
	EXCITADO = 2
	ALERTA = 3
	CONTENTO = 4
	SERENO = 5
	RELAJADO = 6
	CALMADO = 7
	ABURRIDO = 8
	DEPRIMIDO = 9
	INFELIZ = 10
	TRISTE = 11
	TRASTORNADO = 12
	ESTRESADO = 13
	NERVIOSO = 14
	TENSO = 15
	NEGATIVE = 16
	POSITIVE = 17
	INDETERMINADO = 18

def getStrOfSentiment(sentiment):
	if(sentiment == Sentiments.FELIZ.value):
		return 'Feliz'
	elif(sentiment == Sentiments.EXALTADO.value):
		return 'Exaltado'
	elif(sentiment == Sentiments.EXCITADO.value):
		return 'Excitado'
	elif(sentiment == Sentiments.ALERTA.value):
		return 'Alerta'
	elif(sentiment == Sentiments.CONTENTO.value):
		return 'Contento'
	elif(sentiment == Sentiments.SERENO.value):
		return 'Sereno'
	elif(sentiment == Sentiments.RELAJADO.value):
		return 'Relajado'
	elif(sentiment == Sentiments.CALMADO.value):
		return 'Calmado'
	elif(sentiment == Sentiments.ABURRIDO.value):
		return 'Aburrido'
	elif(sentiment == Sentiments.DEPRIMIDO.value):
		return 'Deprimido'
	elif(sentiment == Sentiments.INFELIZ.value):
		return 'Infeliz'
	elif(sentiment == Sentiments.TRISTE.value):
		return 'Triste'
	elif(sentiment == Sentiments.TRASTORNADO.value):
		return 'Transtornado'
	elif(sentiment == Sentiments.ESTRESADO.value):
		return 'Estresado'
	elif(sentiment == Sentiments.NERVIOSO.value):
		return 'Nervioso'
	elif(sentiment == Sentiments.TENSO.value):
		return 'Tenso'
	elif(sentiment == Sentiments.NEGATIVE.value):
		return 'Negativo'
	elif(sentiment == Sentiments.POSITIVE.value):
		return 'Positivo'
	elif(sentiment == Sentiments.INDETERMINADO.value):
		return 'Indeterminado'

def getSentimentPoints():
	xCenter = 5
	yCenter = 5
	radio = 4
	numOfSentiments = 16
	numOfCuadrants = 4
	difAngle = 360 / (numOfSentiments + numOfCuadrants)
	puntos = []
	actualAngle = difAngle
	for i in range(0,numOfCuadrants):
		cuadrante = []
		for j in range(0, numOfSentiments / numOfCuadrants):
			x = math.cos(math.radians(actualAngle)) * radio + xCenter
			y = math.sin(math.radians(actualAngle)) * radio + yCenter
			puntos.append([x,y])
			actualAngle += difAngle
		actualAngle += difAngle	
	return puntos
