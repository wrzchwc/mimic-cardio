import subprocess
from typing import Optional, List

base_url = "https://physionet.org/files/mimic-iv-echo/0.1/"

def fetch_ecg(username: Optional[str],password: Optional[str],dicom_path: str) -> None:
    if not username or not password:
        raise ValueError("Please set PHYSIONET_USERNAME and PHYSIONET_PASSWORD in your .env file")
    try:
        subprocess.run(build_command(username, password, dicom_path), check=True)
        print("Download complete")
    except subprocess.CalledProcessError as e:
        print(f"Failure: {e}")

def build_command(username: str, password: str, dicom_path: str) -> List[str]:
    return [
        "wget",
        "-r",
        "-N",
        "-c",
        "-np",
        "--user", username,
        "--password", password,
        "-P", "../assets",
        f"{base_url}{dicom_path}"
    ]