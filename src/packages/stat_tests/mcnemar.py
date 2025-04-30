from os import makedirs
from json import dumps
from numpy import ndarray, sum
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.multitest import multipletests
from tqdm import tqdm


def mcnemar_test_multi_label(
        y_true: ndarray,
        y_pred1: ndarray,
        y_pred2: ndarray,
        alpha: float,
        labels: list[str],
        prefix: str
):
    n_labels = y_true.shape[1]
    p_values = []
    raw_results = []

    for i in tqdm(range(n_labels), desc=f"McNemar test for {prefix}"):
        correct1 = y_pred1[:, i] == y_true[:, i]
        correct2 = y_pred2[:, i] == y_true[:, i]
        b = sum(correct1 & ~correct2)
        c = sum(~correct1 & correct2)

        matrix = [[0, b], [c, 0]]
        result = mcnemar(matrix, exact=b + c < 25)

        raw_results.append({
            'label': labels[i],
            'b': int(b),
            'c': int(c),
            'statistic': float(result.statistic),
            'p_value': float(result.pvalue)
        })
        p_values.append(result.pvalue)

    reject, pvals_corrected, *_ = multipletests(p_values, alpha=alpha, method='holm')

    for i, res in enumerate(raw_results):
        res['p_corrected'] = float(pvals_corrected[i])
        res['significant'] = bool(reject[i])

    save_results(prefix, raw_results, alpha)


def save_results(prefix: str, results: list, alpha: float):
    path = f'./assets/results/{prefix}'
    makedirs(path, exist_ok=True)
    with open(f'{path}/mcnemar-{alpha}.json', 'w') as file:
        file.write(dumps(results))
