from packages.ecg import fetch_ecg, get_dicom_path
from packages.open_ai import query_model


def main():
    dicom_path = get_dicom_path(
        hadm_id='25618074',
        subject_id='16846280'
    )
    fetch_ecg(dicom_path)
    response = query_model("Tell me a joke!")
    print(response.output_text)