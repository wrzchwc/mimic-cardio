from sys import argv

from sklearn.preprocessing import MultiLabelBinarizer

import packages.diagnoses as diagnoses
from packages.stats import generate_classification_report, generate_accuracy_report

cluster = 'c'


def main():
    cases_path = argv[1]
    prefix = argv[2]
    if cluster in prefix:
        with open('./assets/icd_codes.txt', 'r') as file:
            all_codes = diagnoses.cluster_codes([line.strip() for line in file.readlines()])
        mlb = MultiLabelBinarizer(classes=all_codes)
        diagnoses_for_cases = diagnoses.get_clustered_diagnoses_for_cases(all_codes, cases_path, prefix)
    else:
        with open('./assets/icd_codes.txt', 'r') as file:
            all_codes = [line.strip() for line in file.readlines()]
        mlb = MultiLabelBinarizer(classes=all_codes)
        diagnoses_for_cases = diagnoses.get_diagnoses_for_cases(all_codes, cases_path, prefix)
    y_true, y_pred = diagnoses.encode_diagnoses_for_cases(mlb, diagnoses_for_cases)
    generate_classification_report(y_true, y_pred, all_codes, prefix)
    generate_accuracy_report(y_true, y_pred, mlb.classes_, prefix)
