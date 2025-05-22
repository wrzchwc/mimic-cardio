from os.path import splitext
from sys import argv
from tqdm import tqdm

from packages.cases import load_cases
from packages.ecg import fetch_ecg, get_dicom_path, convert_to_pdf
from packages.open_ai import save_response, TokenManager, build_with_ecg, build, build_short, build_short_with_ecg
from packages.open_ai.case_size_error import CaseSizeError


def main():
    token_manager = TokenManager(argv[3], argv[4])
    cases = load_cases(argv[1])
    for index, case in enumerate(tqdm(cases, argv[2])):
        hadm_id = case['hadm_id']
        dicom_path = get_dicom_path(
            subject_id=case['subject_id'],
            dischtime=case['dischtime']
        )
        model_input = build_input(case, dicom_path)
        try:
            response = token_manager.send_request(model_input, hadm_id)
        except CaseSizeError as e:
            print(e.message)
            continue
        except Exception as e:
            print(e)
            continue
        save_response(
            response=response.output_text,
            hadm_id=hadm_id,
            prefix=argv[2]
        )


def build_input(case: object, dicom_path):
    if dicom_path is None:
        return build(case)
        # return build_short(case)
    else:
        fetch_ecg(dicom_path)
        pdf_filename = convert_to_pdf(dicom_path)
        path = splitext(pdf_filename)[0]
        return build_with_ecg(path, case, pdf_filename)
        # return build_short_with_ecg(path, case, pdf_filename)
