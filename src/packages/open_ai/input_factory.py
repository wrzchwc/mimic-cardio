from json import dumps

from openai import OpenAI

__final_prompt = "Analyse input data and list all possible diagnoses in the form of ICD-10 codes."

__client = OpenAI()


def build_with_ecg(path: str, case: object, ecg_meta: str):
    return [
        {
            "role": "developer",
            "content": __load_text_data('./assets/prompts/dev_ecg')
        },
        {
            "role": "developer",
            "content": __load_text_data('./assets/prompts/dev_json')
        },
        {
            "role": "user",
            "content": f"Here's the JSON data: {dumps(case)}"
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "input_file",
                    "file_id": (__upload_dicom(path))
                },
                {
                    "type": "input_text",
                    "text": f"{__upload_dicom(path)} pdf file contains the result of ECG study - the earliest study the happened closest to dischtime."
                },
            ]
        },
        {
            "role": "user",
            "content": f"Here's the metadata of the ECG: {ecg_meta}"
        },
        {
            "role": "user",
            "content": __final_prompt
        }
    ]


def build(case: object):
    return [
        {
            "role": "developer",
            "content": __load_text_data('./assets/prompts/dev')
        },
        {
            "role": "developer",
            "content": __load_text_data('./assets/prompts/dev_json')
        },
        {
            "role": "user",
            "content": f"Here's the JSON data: {dumps(case)}"
        },
        {
            "role": "user",
            "content": __final_prompt
        }
    ]


def __load_text_data(path: str) -> str:
    with open(f"{path}.txt", "r") as file:
        content = file.read()
    return content


def __upload_dicom(path: str):
    file_object = __client.files.create(
        file=open(f"{path}.pdf", "rb"),
        purpose="user_data"
    )
    return file_object.id
