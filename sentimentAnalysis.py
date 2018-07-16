import json
import matplotlib.pyplot as plt
from stemming.porter2 import stem
from nltk.corpus import stopwords

#----------------------------------Function to get input text to be tested-------------------------------------
def getText():
	text=raw_input("Enter the text : ")
	text=text.replace("\n"," ")
	text=text.replace(".","")
	text=text.replace(",","")
	text=text.replace("\"","")
	text=text.lower()
	text=text.split()
	stopWords = set(stopwords.words('english'))
	filteredText = [w for w in text if not w in stopWords]
	return filteredText

text=getText()

#--------------------------------------Loading hedonometer word dataset-------------------------------------------
tempHedo=open('hedonometer.json')  
tempHedo=json.load(tempHedo)
hedonometerWordDict={}

for p in tempHedo['objects']:
	hedonometerWordDict[p['word']]=(p['happs']-1)*(10/(8))-5	#Normalisation of data

del tempHedo

#-------------------------------------Calculating average happs score----------------------------------------------
happsSum=0
textLen=0
yAxis=[]
for w in text:
	try:
		happsSum+=hedonometerWordDict[w]
		textLen+=1
		yAxis.append(happsSum/textLen)
		continue
	except (KeyError):
		pass

	try:
		happsSum+=hedonometerWordDict[stem(w)]
		textLen+=1
		yAxis.append(happsSum/textLen)
	except (KeyError):
		pass
try:
	avgStress=happsSum/textLen
	print "Final score :",avgStress
	print "Min score :",min(yAxis)

#------------------------------------------------Graph plotting-------------------------------------------------------
	xAxis=range(-1,textLen+2)
	avg=[]
	medium=[]
	high=[]
	critical=[]
	veryCritical=[]
	for x in xAxis:									#Creating reference lines
		avg.append(avgStress)
		medium.append(0.3125)
		high.append(-0.625)
		critical.append(-1.25)
		veryCritical.append(-1.875)

	plt.plot(range(textLen), yAxis,linewidth=2.0)

	plt.plot(xAxis, avg,'k:', label="average stress score")
	plt.plot(xAxis, medium,'g--', label="medium stress")
	plt.plot(xAxis, high,'y--', label="high stress")
	plt.plot(xAxis, critical,'m--', label="critical stress")
	plt.plot(xAxis, veryCritical,'r--', label="very critical stress")

	plt.legend()

	plt.xlabel('Number of Words')
	plt.ylabel('Stress level')
	plt.axis([-1, textLen+1, min(yAxis)-1, max(yAxis)+1])

	plt.show()

except (ZeroDivisionError):
	print "Text Length Invalid"