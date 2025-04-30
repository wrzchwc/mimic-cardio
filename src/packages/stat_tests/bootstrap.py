import numpy as np
from sklearn.metrics import recall_score
from tqdm import tqdm

resamples = 68_840

def bootstrap_sample_recall(y_true, y_pred, alpha: float, prefix: str):
    assert y_true.shape == y_pred.shape
    n = y_true.shape[0]
    recalls = []
    for _ in tqdm(range(resamples), desc="Bootstrapping sample recall"):
        indices = np.random.choice(n, size=n, replace=True)
        y_true_boot = y_true[indices]
        y_pred_boot = y_pred[indices]
        recall = recall_score(y_true_boot, y_pred_boot, average='samples', zero_division=0)
        recalls.append(recall)
    recalls = np.array(recalls)
    mean_recall = float(np.mean(recalls))
    ci_lower = float(np.percentile(recalls, alpha / 2 * 100))
    ci_upper = float(np.percentile(recalls, 100 - alpha / 2 * 100))
    save_results(prefix, mean_recall, ci_lower, ci_upper)


def save_results(prefix: str, mean_recall: float, ci_lower: float, ci_upper: float):
    with open(f'./assets/results/{prefix}/bootstrap-sample-recall.txt', 'w') as file:
        file.write('mean_recall, ci_lower, ci_upper\n')
        file.write(f'{mean_recall}, {ci_lower}, {ci_upper}\n')
