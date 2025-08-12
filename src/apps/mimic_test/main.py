from collections import Counter
from sys import argv

from sklearn.preprocessing import MultiLabelBinarizer
from packages.diagnoses import *
from packages.stat_tests import mcnemar_test_multi_label, wilcoxon_signed_pair_test, bootstrap_sample_recall


def main():
    experiment_1 = argv[2]
    experiment_2 = argv[3]
    hadm_ids = []
    for experiment in [experiment_1, experiment_2]:
        hadm_ids.append(get_hadm_ids_from_responses(experiment))
    if not Counter(hadm_ids[0]) == Counter(hadm_ids[1]):
        raise Exception('hadm_ids do not match!')
    cluster = len(argv) == 5 and argv[4] == 'c'
    codes = get_codes(cluster)
    mlb = get_binarizer(cluster, codes)
    y_true = mlb.fit_transform(original_diagnoses(cluster, codes))
    y_pred_1 = mlb.transform(predicted_diagnoses(cluster, codes, experiment_1))
    y_pred_2 = mlb.transform(predicted_diagnoses(cluster, codes, experiment_2))
    prefix = f'{experiment_1}_{experiment_2}{f"_{argv[4]}" if cluster else ""}'
    alpha = float(argv[1])
    mcnemar_test_multi_label(y_true, y_pred_1, y_pred_2, alpha, codes, prefix)
    wilcoxon_signed_pair_test(y_true, y_pred_1, y_pred_2, alpha, 'less', prefix)
    bootstrap_sample_recall(y_true, y_pred_1, alpha, f'{experiment_1}{f"{argv[4]}" if cluster else ""}')
    bootstrap_sample_recall(y_true, y_pred_2, alpha, f'{experiment_2}{f"{argv[4]}" if cluster else ""}')


def get_codes(cluster: bool) -> list[str]:
    if cluster:
        return cluster_codes(load_codes())
    return load_codes()


def get_binarizer(cluster: bool, codes: list[str]) -> MultiLabelBinarizer:
    if cluster:
        return MultiLabelBinarizer(classes=cluster_codes(codes))
    return MultiLabelBinarizer(classes=codes)


def original_diagnoses(cluster: bool, codes: list[str]):
    if cluster:
        return get_clustered_original_diagnoses(codes, argv[2])
    return get_original_diagnoses(codes, argv[2])


def predicted_diagnoses(cluster: bool, codes: list[str], prefix: str):
    if cluster:
        return get_clustered_predicted_diagnoses(codes, prefix)
    return get_predicted_diagnoses(codes, prefix)
