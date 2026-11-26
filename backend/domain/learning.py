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
    if 'bowl_points' in data:
        return calculate_bowl(data)
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


def calculate_bowl(data):
    # 同一碗颜料只能给一个比例：逐点预测后先剔除任一点区间过宽的比例档，
    # 再在剩余比例中选择“最差点色差上界”最低的一档（minimax 上界）。
    rows = sorted(data['studies'], key=lambda row: (row['fraction'], row['ground_l'], row['code']))
    holdout = rows[::5]
    training = [row for i, row in enumerate(rows) if i % 5]
    hold_X = feature_matrix([row['fraction'] for row in holdout], [row['ground_l'] for row in holdout])
    truth = [row['delta_e'] for row in holdout]
    mae = float(mean_absolute_error(truth, model_fit(training).predict(hold_X)))

    extent = [row['fraction'] for row in rows]
    fractions = np.linspace(min(extent), max(extent), 41)
    fitted = model_fit(rows)

    point_results = []
    # 每格的最差上界与可行标记，跨点汇总后再选档
    worst_upper = np.zeros(fractions.shape)
    feasible = np.ones(fractions.shape, dtype=bool)
    for point in data['bowl_points']:
        candidate_X = feature_matrix(fractions, np.full(fractions.shape, point['ground_l']))
        means, std = fitted.predict(candidate_X, return_std=True)
        lower = np.maximum(0., means - 1.96 * std)
        upper = means + 1.96 * std
        width = upper - lower
        width_ok = width <= 3.0
        feasible &= width_ok
        worst_upper = np.maximum(worst_upper, upper)
        point_results.append({'x_mm': point['x_mm'], 'y_mm': point['y_mm'],
            'ground_l': float(point['ground_l']),
            'grid': [{'fraction': round(float(f), 5), 'mean': round(float(m), 5),
                      'lower': round(float(lo), 5), 'upper': round(float(up), 5),
                      'width': round(float(w), 5), 'width_ok': bool(ok)}
                     for f, m, lo, up, w, ok in
                     zip(fractions, means, lower, upper, width, width_ok)]})

    if not feasible.any():
        raise ValueError('每个候选比例都至少在一个点上预测区间过宽，先补采干样')
    feasible_index = np.where(feasible)[0]
    selected = int(feasible_index[np.argmin(worst_upper[feasible_index])])

    points = []
    means_at_selected = []
    lower_at_selected = []
    upper_at_selected = []
    for point, item in zip(data['bowl_points'], point_results):
        cell = item['grid'][selected]
        points.append({'x_mm': point['x_mm'], 'y_mm': point['y_mm'],
            'ground_l': float(point['ground_l']), 'fraction': cell['fraction'],
            'mean_de': cell['mean'], 'lower_de': cell['lower'],
            'upper_de': cell['upper'], 'width_de': cell['width']})
        means_at_selected.append(cell['mean'])
        lower_at_selected.append(cell['lower'])
        upper_at_selected.append(cell['upper'])

    # 备选仅保留通过区间宽度筛选的比例，按最差上界从低到高展示前四档
    ranked = feasible_index[np.argsort(worst_upper[feasible_index])][:4]
    candidates = [{'fraction': round(float(fractions[i]), 5),
                   'worst_upper': round(float(worst_upper[i]), 5)} for i in ranked]
    return {'fraction': round(float(fractions[selected]), 5),
        'mean_de': round(float(np.mean(means_at_selected)), 5),
        'lower_de': round(float(min(lower_at_selected)), 5),
        'upper_de': round(float(max(upper_at_selected)), 5),
        'max_upper_de': round(float(worst_upper[selected]), 5),
        'test_mae': round(mae, 6), 'train': len(training), 'holdout': len(holdout),
        'points': points, 'candidates': candidates}
