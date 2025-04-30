from sklearn.preprocessing import MultiLabelBinarizer
from numpy import ndarray


def encode_original_diagnoses_for_cases(mlb: MultiLabelBinarizer, diagnoses_for_cases: list[list[str]]) -> ndarray:
    return mlb.fit_transform(diagnoses_for_cases)


def encode_predicted_diagnoses_for_cases(mlb: MultiLabelBinarizer, diagnoses_for_cases: list[list[str]]) -> ndarray:
    return mlb.transform(diagnoses_for_cases)
