import json

from openai import OpenAI
from openai.types.responses import Response

client = OpenAI()


def query_model(path: str, case: object, model: str = "gpt-4.1-nano") -> Response:
    return client.responses.create(
        model=model,
        input=build_input(
            dicom_id=upload_dicom(path),
            case=case,
            ecg_meta=load_ecg_meta(path)
        ),
        text=load_schema(),
        temperature=0.1
    )


def upload_dicom(path: str):
    file_object = client.files.create(
        file=open(f"{path}.pdf", "rb"),
        purpose="user_data"
    )
    return file_object.id


def load_ecg_meta(path: str):
    with open(f"{path}.txt", "r") as file:
        content = file.read()
    return content


def build_input(dicom_id: str, case: object, ecg_meta: str):
    return [
        {
            "role": "developer",
            "content": "You will receive PDF containing ECG study, metadata of the ECG and JSON data describing patient hospitalization."
        },
        {
            "role": "developer",
            "content": "Your task will be to analyse the input data and list all possible diagnoses in the form of ICD-10 codes"
        },
        {
            "role": "developer",
            "content": "Do not summarise most important information about patient or hospitalization"
        },
        {
            "role": "developer",
            "content": "Briefly refer to facts leading to the diagnoses"
        },
        {
            "role": "user",
            "content": f"Here's the JSON data: {json.dumps(case)}"
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "input_file",
                    "file_id": dicom_id
                },
                {
                    "type": "input_text",
                    "text": f"{dicom_id} pdf file contains the result of ECG study - the earliest study the happened closest to dischtime."
                },
            ]
        },
        {
            "role": "user",
            "content": f"Here's the metadata of the ECG: {ecg_meta}"
        },
        {
            "role": "user",
            "content": "Analyse input data and list all possible diagnoses in the form of ICD-10 codes."
        }
    ]


def load_schema():
    with open('./assets/schema.json', 'r') as file:
        return json.load(file)
