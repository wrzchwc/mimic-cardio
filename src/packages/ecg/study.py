from typing import TypedDict
from .dicom import Dicom


class Study(TypedDict):
    study_id: int
    subject_id: int
    study_datetime: str
    dicoms: list[Dicom]