from sys import argv

from sklearn.preprocessing import MultiLabelBinarizer

from packages.diagnoses import encode_original_diagnoses_for_cases, encode_predicted_diagnoses_for_cases, cluster_codes, \
    load_codes, get_clustered_diagnoses_for_cases, get_original_diagnoses, get_predicted_diagnoses
from packages.stats import generate_classification_report, generate_accuracy_report

cluster = 'c'


def main():
    cases_path = argv[1]
    prefix = argv[2]
    if cluster in prefix:
        all_codes = cluster_codes(load_codes())
        mlb = MultiLabelBinarizer(classes=all_codes)
        original_diagnoses, predicted_diagnoses = get_clustered_diagnoses_for_cases(all_codes, cases_path, prefix)
    else:
        all_codes = load_codes()
        mlb = MultiLabelBinarizer(classes=all_codes)
        original_diagnoses = get_original_diagnoses(all_codes, prefix)
        predicted_diagnoses = get_predicted_diagnoses(all_codes, prefix)
    y_true = encode_original_diagnoses_for_cases(mlb, original_diagnoses)
    y_pred = encode_predicted_diagnoses_for_cases(mlb, predicted_diagnoses)
    generate_classification_report(y_true, y_pred, all_codes, prefix)
    generate_accuracy_report(y_true, y_pred, mlb.classes_, prefix)
