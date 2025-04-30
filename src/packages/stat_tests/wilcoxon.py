from os import makedirs

from numpy import array
from scipy.stats import wilcoxon
from sklearn.metrics import recall_score


def wilcoxon_signed_pair_test(y_true, y_pred1, y_pred2, alpha: float, alternative: str, prefix: str):
    recall1 = sample_level_recall(y_true, y_pred1)
    recall2 = sample_level_recall(y_true, y_pred2)
    result = wilcoxon(recall1, recall2, alternative=alternative)
    statistic = float(result.statistic)
    pvalue = float(result.pvalue)
    significant = pvalue < alpha
    save_results(prefix, (statistic, pvalue, significant), alpha)


def sample_level_recall(y_true, y_pred):
    recalls = []
    for true, pred in zip(y_true, y_pred):
        recalls.append(recall_score(true, pred, zero_division=1))
    return array(recalls)


def save_results(prefix: str, results: tuple, alpha: float):
    path = f'./assets/results/{prefix}'
    makedirs(path, exist_ok=True)
    with open(f'{path}/wilcoxon-{alpha}.txt', 'w') as file:
        file.write('(statistic, pvalue, significant)\n')
        file.write(str(results))
