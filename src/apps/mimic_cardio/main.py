from os.path import splitext
from datetime import datetime
from sys import argv

from packages.cases import load_cases
from packages.ecg import fetch_ecg, get_dicom_path, convert_to_pdf
from packages.open_ai import query_model, save_response, query_model_with_ecg

model = "gpt-4.1-2025-04-14"


def main():
    print(argv[1:])
    cases = load_cases(argv[1])
    for index, case in enumerate(cases):
        hadm_id = case['hadm_id']
        print(f"index: {index}, hadm_id: {hadm_id}")
        dicom_path = get_dicom_path(
            subject_id=case['subject_id'],
            dischtime=case['dischtime']
        )
        if dicom_path is None:
            response, time = query(case)
        else:
            response, time = query_with_ecg(case, dicom_path)
        print(f"time: {time}")
        save_response(
            response=response.output_text,
            hadm_id=hadm_id,
            prefix=argv[2],
            time=time
        )


def query(case: object):
    print('Querying model')
    start = datetime.now()
    response = query_model(case, model)
    end = datetime.now()
    time = calculate_time(start, end)
    return response, time


def query_with_ecg(case: object, dicom_path: str):
    print('Downloading ECG')
    fetch_ecg(dicom_path)
    print('Converting DICOM to PDF')
    pdf_filename = convert_to_pdf(dicom_path)
    path = splitext(pdf_filename)[0]
    print('Querying model')
    start = datetime.now()
    response = query_model_with_ecg(path, case, model)
    end = datetime.now()
    time = calculate_time(start, end)
    return response, time


def calculate_time(start: datetime, end: datetime) -> float:
    diff = end - start
    return diff.total_seconds()
