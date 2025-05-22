from collections import Counter

from sklearn.preprocessing import MultiLabelBinarizer
from packages.diagnoses import get_hadm_ids_from_responses, load_codes, get_original_diagnoses, get_predicted_diagnoses
from packages.stat_tests import mcnemar_test_multi_label, wilcoxon_signed_pair_test, bootstrap_sample_recall


def main():
    experiment_1 = 'e6'
    experiment_2 = 'e4'
    alpha = 0.05
    hadm_ids = []
    for experiment in [experiment_1, experiment_2]:
        hadm_ids.append(get_hadm_ids_from_responses(experiment))
    if not Counter(hadm_ids[0]) == Counter(hadm_ids[1]):
        raise Exception('hadm_ids do not match!')
    codes = load_codes()
    mlb = MultiLabelBinarizer(classes=codes)
    original_diagnoses = get_original_diagnoses(codes, experiment_1)
    y_true = mlb.fit_transform(original_diagnoses)
    y_pred_1 = mlb.transform(get_predicted_diagnoses(codes, experiment_1))
    y_pred_2 = mlb.transform(get_predicted_diagnoses(codes, experiment_2))
    prefix = f'{experiment_1}_{experiment_2}'
    mcnemar_test_multi_label(y_true, y_pred_1, y_pred_2, alpha, codes, prefix)
    wilcoxon_signed_pair_test(y_true, y_pred_1, y_pred_2, alpha, 'greater', prefix)
    bootstrap_sample_recall(y_true, y_pred_1, alpha, experiment_1)
    bootstrap_sample_recall(y_true, y_pred_2, alpha, experiment_2)

