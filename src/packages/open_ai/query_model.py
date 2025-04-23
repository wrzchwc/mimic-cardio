import json

from openai import OpenAI
from openai.types.responses import Response

client = OpenAI()

default_model = "gpt-4.1-nano"
temperature = 0.1

final_prompt = "Analyse input data and list all possible diagnoses in the form of ICD-10 codes."


def query_model_with_ecg(path: str, case: object, model: str = default_model) -> Response:
    return client.responses.create(
        model=model,
        input=build_input_with_ecg(
            case=case,
            dicom_id=upload_dicom(path),
            ecg_meta=load_text_data(path)
        ),
        text=load_schema(),
        temperature=temperature
    )


def query_model(case: object, model: str = default_model) -> Response:
    return client.responses.create(
        model=model,
        input=build_input(case),
        text=load_schema(),
        temperature=temperature
    )


def upload_dicom(path: str):
    file_object = client.files.create(
        file=open(f"{path}.pdf", "rb"),
        purpose="user_data"
    )
    return file_object.id


def build_input_with_ecg(dicom_id: str, case: object, ecg_meta: str):
    return [
        {
            "role": "developer",
            "content": load_text_data('./assets/prompts/dev_ecg')
        },
        {
            "role": "developer",
            "content": load_text_data('./assets/prompts/dev_json')
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
            "content": final_prompt
        }
    ]


def build_input(case: object):
    return [
        {
            "role": "developer",
            "content": load_text_data('./assets/prompts/dev')
        },
        {
            "role": "developer",
            "content": load_text_data('./assets/prompts/dev_json')
        },
        {
            "role": "user",
            "content": f"Here's the JSON data: {json.dumps(case)}"
        },
        {
            "role": "user",
            "content": final_prompt
        }
    ]


def load_text_data(path: str) -> str:
    with open(f"{path}.txt", "r") as file:
        content = file.read()
    return content


def load_schema():
    with open('./assets/schema.json', 'r') as file:
        return json.load(file)
