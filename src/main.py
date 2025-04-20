from dotenv import load_dotenv
from os import getenv

from src.fetch_ecg import fetch_ecg

load_dotenv()

if __name__ == "__main__":
    username = getenv("PHYSIONET_USERNAME")
    password = getenv("PHYSIONET_PASSWORD")
    dicom_path = "files/p16/p16846280/s96459668/96459668_0001.dcm"
    fetch_ecg(username, password, dicom_path)