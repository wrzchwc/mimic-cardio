from os.path import splitext
from datetime import datetime
from sys import argv

from packages.cases import load_cases
from packages.ecg import fetch_ecg, get_dicom_path, convert_to_pdf
from packages.open_ai import save_response, TokenManager, build_with_ecg, build
from packages.open_ai.case_size_error import CaseSizeError


def main():
    token_manager = TokenManager('o3-2025-04-16', 30_000)
    cases = [case for case in load_cases(argv[1]) if case['hadm_id'] not in ('25102602')]
    for index, case in enumerate(cases):
        hadm_id = case['hadm_id']
        print(f"index: {index}, hadm_id: {hadm_id}")
        dicom_path = get_dicom_path(
            subject_id=case['subject_id'],
            dischtime=case['dischtime']
        )
        model_input = build_input(case, dicom_path)
        start = datetime.now()
        try:
            response = token_manager.send_request(model_input, hadm_id)
        except CaseSizeError as e:
            print(e.message)
            continue
        end = datetime.now()
        save_response(
            response=response.output_text,
            hadm_id=hadm_id,
            prefix=argv[2],
            time=(end - start).total_seconds()
        )


def build_input(case: object, dicom_path: str | None):
    if dicom_path is None:
        return build(case)
    else:
        print('Downloading ECG')
        fetch_ecg(dicom_path)
        print('Converting DICOM to PDF')
        pdf_filename = convert_to_pdf(dicom_path)
        path = splitext(pdf_filename)[0]
        return build_with_ecg(path, case, pdf_filename)
