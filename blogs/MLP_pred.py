def Predict_from_thsese_(given_data):
	import mglearn
	import numpy as np
	import matplotlib.pyplot as plt
	import pandas as pd
	from sklearn.neural_network import MLPRegressor
	import pickle
	import csv


    mlp = pickle.load(open('static/data/finalized_model.sav', 'rb'))

	with open('static/data/Xmean.csv') as f:
	    reader = csv.reader(f)
	    Xmean = [row for row in reader]
	Xmean = np.array(Xmean).astype('float64')
	
	with open('static/data/Xstd.csv') as f:
	    reader = csv.reader(f)
	    Xstd = [row for row in reader]
	Xstd = np.array(Xstd).astype('float64')

	Ymean = 92.68061322261258
	Ystd = 19.06101964452713

	EX = np.empty((given_data.shape))
	for col in [0,3,4,5,6,7,8,9,10,11]:
		z_score = (given_data[:,col] - Xmean[col])/Xstd[col]
		EX[:,col] = z_score
	EX[:,1] = given_data[:,1]
	EX[:,2] = given_data[:,2]
	EX[:,12] = given_data[:,12]

	Predicted_data = mlp.predict(EX)

	return(Predicted_data*Ystd + Ymean)


