from os import getenv
from subprocess import run, CalledProcessError
from typing import List

username = getenv("PHYSIONET_USERNAME")
password = getenv("PHYSIONET_PASSWORD")

base_url = "https://physionet.org/files/mimic-iv-echo/0.1/"

def fetch_ecg(dicom_path: str) -> None:
    if not username or not password:
        raise ValueError("Please set PHYSIONET_USERNAME and PHYSIONET_PASSWORD in your .env file")
    try:
        run(build_command(username, password, dicom_path), check=True)
    except CalledProcessError as e:
        print(f"ECG download failure: {e}")

def build_command(username: str, password: str, dicom_path: str) -> List[str]:
    return [
        "wget",
        "-r",
        "-N",
        "-c",
        "-np",
        "--user", username,
        "--password", password,
        "-P", "./assets",
        "--quiet",
        f"{base_url}{dicom_path}"
    ]