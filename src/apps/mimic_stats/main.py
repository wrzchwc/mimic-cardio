from sys import argv

from sklearn.preprocessing import MultiLabelBinarizer

from packages.diagnoses import get_diagnoses_for_cases, encode_diagnoses_for_cases
from packages.stats import generate_classification_report, generate_accuracy_report


def main():
    cases_path = argv[1]
    prefix = argv[2]
    with open('./assets/icd_codes.txt', 'r') as file:
        all_codes = [line.strip() for line in file.readlines()]
    mlb = MultiLabelBinarizer(classes=all_codes)
    y_true, y_pred = encode_diagnoses_for_cases(mlb, get_diagnoses_for_cases(all_codes, cases_path, prefix))
    generate_classification_report(y_true, y_pred, all_codes, prefix)
    generate_accuracy_report(y_true, y_pred, mlb.classes_, prefix)
