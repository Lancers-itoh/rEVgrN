
def normalization(values_as_nparr, XmeanCsvPath, XstdCsvPath):
    import csv
    import numpy as np
    with open(XmeanCsvPath) as f:
        reader = csv.reader(f)
        Xmean = [row for row in reader]
    Xmean = np.array(Xmean).astype('float64')
    
    with open(XstdCsvPath) as f:
        reader = csv.reader(f)
        Xstd = [row for row in reader]
    Xstd = np.array(Xstd).astype('float64')

    EX = list(range(len(values_as_nparr)))
    for col in [0,3,4,5,6,7,8,9,10,11]:
        z_score = (values_as_nparr[col] - Xmean[0,col])/Xstd[0,col]
        EX[col] = z_score
    EX[1] = values_as_nparr[1]
    EX[2] = values_as_nparr[2]
    EX[12] = values_as_nparr[12]

    return(EX)

def Predict_from_these(given_data, ModelPath, Ymean, Ystd):
    import pickle
    import numpy as np
    from sklearn.neural_network import MLPRegressor
    loaded_model = pickle.load(open(ModelPath, 'rb'))
    EX = np.array(given_data).reshape(1,13)
    Predicted_data = loaded_model.predict(EX)
    return(Predicted_data*Ystd + Ymean)




 