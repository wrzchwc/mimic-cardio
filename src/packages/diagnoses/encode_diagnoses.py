from sklearn.preprocessing import MultiLabelBinarizer


def encode_diagnoses_for_cases(mlb: MultiLabelBinarizer, diagnoses_for_cases: tuple[list[str], list[str]]) -> tuple:
    y_true = mlb.fit_transform(diagnoses_for_cases[0])
    y_pred = mlb.transform(diagnoses_for_cases[1])
    return y_true, y_pred
