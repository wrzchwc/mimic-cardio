from os import makedirs
from sklearn.metrics import classification_report


def generate_classification_report(y_true, y_pred, target_names: list[str], prefix: str):
    report = classification_report(y_true, y_pred, target_names=target_names, zero_division=0)
    path = f'./assets/results/{prefix}'
    makedirs(path, exist_ok=True)
    with open(f'{path}/classification_report.txt', 'w') as file:
        file.write(report)
