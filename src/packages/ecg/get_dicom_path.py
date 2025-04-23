from json import loads

from .study import Study


def get_dicom_path(subject_id: str, dischtime: str) -> str | None:
    study = get_latest_study(subject_id, dischtime)
    if study is None:
        return None
    return study.get('dicoms')[0].get('dicom_filepath')


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
