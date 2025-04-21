from json import loads

from .case import Case
from .study import Study


def get_dicom_path(hadm_id: str, subject_id: str) -> str:
    case = get_case(hadm_id)
    study = get_latest_study(subject_id, case.get('dischtime'))
    return study.get('dicoms')[0].get('dicom_filepath')


def get_case(hadm_id: str) -> Case:
    cases = []
    with open('./assets/cases.jsonl', 'r') as file:
        for case in file:
            case = loads(case)
            cases.append({
                "hadm_id": (case['hadm_id']),
                "dischtime": (case['dischtime'])
            })
    return next((case for case in cases if case['hadm_id'] == hadm_id), None)


def get_latest_study(subject_id: str, dischtime: str) -> Study:
    studies: list[Study] = []
    with open('./assets/echo.jsonl', 'r') as file:
        for study in file:
            study = loads(study)
            studies.append({
                "study_id": (study['study_id']),
                "subject_id": (study['subject_id']),
                "study_datetime": (study['study_datetime']),
                "dicoms": (study['dicoms'])
            })
    return next(
        (study for study in studies if study['subject_id'] == subject_id and study['study_datetime'] <= dischtime),
        None
    )
