from pyAudioAnalysis import audioTrainTest as aT
import pickle
import os
from pydub import AudioSegment
def main(file):


	sound = AudioSegment.from_mp3(file)
	sound.export("output.wav", format="wav")

	index, prob, emo = aT.fileClassification("output.wav", "svmSMtemp","svm")
	print index, prob, emo
	weight = [1, -0.25, 2, -2, -0.5, -2, -0.5, 1]
	for i, j in enumerate(prob):
	    prob[i] *= weight[i]

	os.remove('output.wav')

	score =  sum(prob)
	if score > 0:
		return "The person is not depressed. Their score is " + str(score)

	elif score > -0.4:
		return "The person is moderately depressed. Their score is " + str(score)

	else:
		return "The person is severely depressed. Their score is " + str(score)