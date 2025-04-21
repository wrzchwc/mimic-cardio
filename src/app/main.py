from packages.ecg import fetch_ecg
from packages.open_ai import query_model

def main():
    dicom_path = "files/p16/p16846280/s96459668/96459668_0001.dcm"
    fetch_ecg(dicom_path)
    response = query_model("Tell me a joke!")
    print(response.output_text)