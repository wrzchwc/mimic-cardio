from os import makedirs

from numpy import ndarray, dtype, mean
from sklearn.metrics import accuracy_score, hamming_loss, multilabel_confusion_matrix


def generate_accuracy_report(y_true, y_pred, classes: ndarray[tuple[int], dtype], prefix: str):
    subset_accuracy = accuracy_score(y_true, y_pred, normalize=True, sample_weight=None)
    hamming_accuracy = 1 - hamming_loss(y_true, y_pred)
    label_accuracies = get_label_accuracies(y_true, y_pred)
    mean_label_accuracy = mean(label_accuracies)
    path = f'./assets/results/{prefix}'
    makedirs(path, exist_ok=True)
    with open(f'{path}/accuracy_report.txt', 'w') as file:
        file.write(f'Subset accuracy: {subset_accuracy:.2f}\n')
        file.write(f'Hamming accuracy: {hamming_accuracy:.2f}\n')
        file.write(f'Mean label accuracy: {mean_label_accuracy:.2f}\n')
        file.write('Label accuracies:\n')
        for i, c in enumerate(classes):
            file.write(f'{c}: {label_accuracies[i]:.2f}\n')


def get_label_accuracies(y_true, y_pred) -> list[float]:
    mcm = multilabel_confusion_matrix(y_true, y_pred)
    accuracies = []
    for i, matrix in enumerate(mcm):
        tn, fp, fn, tp = matrix.ravel()
        acc = (tp + tn) / (tp + tn + fp + fn)
        accuracies.append(acc)
    return accuracies
