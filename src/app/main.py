from os.path import splitext
from datetime import datetime

from packages.cases import load_cases
from packages.ecg import fetch_ecg, get_dicom_path, convert_to_pdf
from packages.open_ai import query_model, save_response


def main():
    cases = load_cases()
    for index, case in enumerate(cases):
        hadm_id = case['hadm_id']
        print(f"index: {index}, hadm_id: {hadm_id}")
        dicom_path = get_dicom_path(
            subject_id=case['subject_id'],
            dischtime=case['dischtime']
        )
        print('Downloading ECG')
        fetch_ecg(dicom_path)
        print('Converting DICOM to PDF')
        pdf_filename = convert_to_pdf(dicom_path)
        path = splitext(pdf_filename)[0]
        print('Querying model')
        start = datetime.now()
        response = query_model(path, case, "gpt-4.1")
        end = datetime.now()
        time=(end - start).total_seconds()
        print(f"time: {time}")
        save_response(
            response=response.output_text,
            hadm_id=hadm_id,
            prefix='e',
            time=time
        )
