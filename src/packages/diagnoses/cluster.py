from .diagnoses_for_cases import filter_codes
from packages.cases import load_cases
from json import loads


def get_clustered_diagnoses_for_cases(
        eligible_codes: list[str],
        cases_file: str,
        prefix: str
) -> tuple[list[str], list[str]]:
    with open('./assets/diagnoses.json', 'r') as file:
        original_diagnoses = loads(file.read())
    predicted_diagnoses_for_cases = []
    original_diagnoses_for_cases = []
    hadm_ids = [case['hadm_id'] for case in (load_cases(cases_file))]
    for hadm_id in hadm_ids:
        original_diagnoses_for_case = get_clustered_original_diagnoses_for_case(
            original_diagnoses,
            eligible_codes,
            hadm_id
        )
        if original_diagnoses is None:
            raise Exception(f'No diagnoses found for admission: {hadm_id}')
        original_diagnoses_for_cases.append(original_diagnoses_for_case)
        predicted_diagnoses_for_case = load_clustered_predicted_diagnoses_for_case(hadm_id, eligible_codes, prefix)
        predicted_diagnoses_for_cases.append(predicted_diagnoses_for_case)
    return original_diagnoses_for_cases, predicted_diagnoses_for_cases


def get_clustered_original_diagnoses_for_case(
        all_original_diagnoses: list,
        eligible_codes: list[str],
        hadm_id: str
) -> list[str] | None:
    original_diagnoses = next((d['diagnoses'] for d in all_original_diagnoses if d['hadm_id'] == hadm_id), None)
    return filter_codes(eligible_codes, cluster_codes(original_diagnoses))


def load_clustered_predicted_diagnoses_for_case(hadm_id: str, eligible_codes: list[str], prefix: str) -> list[str]:
    with open(f'./assets/responses/{prefix[:-1]}/{hadm_id}.json', 'r') as file:
        response = loads(file.read())
    diagnoses = [diagnose['code'] for diagnose in response['diagnoses']]
    return filter_codes(eligible_codes, cluster_codes(diagnoses))


def cluster_codes(codes: list[str]) -> list[str]:
    return sorted(set([code[:3] for code in codes]))
