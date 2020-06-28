import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
import pickle

def parse_from_horsedata():

    def delete_last(txt):
        return(txt[:-1])

    def split_by_slash(txt):
        return(re.split('[/]',txt))
    
    ex_data = list(Learningdata.objects.values_list('horse_data', flat=True))
    res_data = list(Learningdata.objects.values_list('time_result', flat = True))
    ex_data = list(map(delete_last, ex_data))
    ex_data = list(map(split_by_slash, ex_data))
    ex = np.array(ex_data).astype("float64")
    res = np.array(res_data).astype("float64")

    Xmean = np.mean(ex,axis=0)
    Xstd = np.std(ex, axis=0)

    Ymean = np.mean(res,axis=0)
    Ystd = np.std(res, axis=0)

    for col in [0,3,4,5,6,7,8,9,10,11,12]:
        z_score = (ex[:,col] - Xmean[col])/Xstd[col]
        ex[:,col] = z_score

    res = (res - Ymean)/Ystd

    X_train, X_test, y_train, y_test = train_test_split(ex, res, random_state=42)
    mlp = MLPRegressor(random_state=0, max_iter=1000, alpha=0.01, hidden_layer_sizes=[100,100], activation="identity",solver='sgd', batch_size=128)
    mlp.fit(X_train, y_train)
    testscore = mlp.score(X_test, y_test)

    Learningdata.objects.update(Xmean = Xmean, Xstd = Xstd, Ymean = Ymean, Ystd = Ystd, test_score = testscore)
    filename = 'static/data/mlp_model.sav'
    pickle.dump(mlp, open(filename, 'wb'))

