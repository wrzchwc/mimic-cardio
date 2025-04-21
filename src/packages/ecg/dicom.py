from typing import TypedDict


class Dicom(TypedDict):
    acquisition_datetime: str
    dicom_filepath: str