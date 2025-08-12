from json import loads
from .get_hadm_ids import get_hadm_ids_from_responses


def get_original_diagnoses(eligible_codes: list[str], prefix: str) -> list[list[str]]:
    with open('./assets/diagnoses.json', 'r') as file:
        all_original_diagnoses = loads(file.read())
    original_diagnoses_for_cases = []
    hadm_ids = get_hadm_ids_from_responses(prefix)
    for hadm_id in hadm_ids:
        original_diagnoses = next((d['diagnoses'] for d in all_original_diagnoses if d['hadm_id'] == hadm_id), None)
        diagnoses_transformed = [d[:3] + '.' + d[3:] for d in original_diagnoses]
        original_diagnoses_for_case = filter_codes(eligible_codes, diagnoses_transformed)
        original_diagnoses_for_cases.append(original_diagnoses_for_case)
    return original_diagnoses_for_cases


def get_predicted_diagnoses(eligible_codes: list[str], prefix: str) -> list[list[str]]:
    predicted_diagnoses_for_cases = []
    hadm_ids = get_hadm_ids_from_responses(prefix)
    for hadm_id in hadm_ids:
        with open(f'./assets/responses/{prefix}/{hadm_id}.json', 'r') as file:
            response = loads(file.read())
        filtered_response = filter_codes(eligible_codes, [diagnose['code'] for diagnose in response['diagnoses']])
        predicted_diagnoses_for_cases.append(sorted(filtered_response))
    return predicted_diagnoses_for_cases


def filter_codes(eligible_codes: list[str], codes: list[str]):
    return [code for code in codes if code in eligible_codes]
