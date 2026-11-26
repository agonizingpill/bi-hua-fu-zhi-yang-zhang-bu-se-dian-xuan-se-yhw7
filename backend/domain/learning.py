import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel
from sklearn.metrics import mean_absolute_error


def feature_matrix(fraction, ground):
    return np.column_stack([np.asarray(fraction,dtype=float), (np.asarray(ground,dtype=float)-50)/25])


def model_fit(rows):
    features = feature_matrix([row['fraction'] for row in rows],[row['ground_l'] for row in rows])
    outputs = [row['delta_e'] for row in rows]
    kernel = Matern(length_scale=[.32,.38], nu=1.5) + WhiteKernel(noise_level=.004)
    return GaussianProcessRegressor(kernel=kernel, optimizer=None, alpha=1e-6,
        normalize_y=True, random_state=1089).fit(features, outputs)


def calculate(data):
    rows = sorted(data['studies'], key=lambda row: (row['fraction'],row['ground_l'],row['code']))
    holdout = rows[::5]
    training = [row for i,row in enumerate(rows) if i%5]
    hold_X = feature_matrix([row['fraction'] for row in holdout],[row['ground_l'] for row in holdout])
    truth = [row['delta_e'] for row in holdout]
    mae = float(mean_absolute_error(truth,model_fit(training).predict(hold_X)))
    extent = [row['fraction'] for row in rows]
    fractions = np.linspace(min(extent),max(extent),41)
    candidate_X = feature_matrix(fractions,np.full(fractions.shape,data['ground_l']))
    means,std = model_fit(rows).predict(candidate_X, return_std=True)
    scores = means + .8*std
    selected = int(np.argmin(scores))
    mean = float(means[selected])
    interval = 1.96*float(std[selected])
    alternatives = [{'fraction':round(float(fractions[index]),5),'mean':round(float(means[index]),5),
        'upper': round(float(means[index]+1.96*std[index]),5)} for index in np.argsort(scores)[:4]]
    return {'fraction':round(float(fractions[selected]),5),'mean_de':round(mean,5),
        'lower_de':round(max(0.,mean-interval),5),'upper_de':round(mean+interval,5),
        'test_mae':round(mae,6),'train':len(training),'holdout':len(holdout),
        'candidates':alternatives}
