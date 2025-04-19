import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("PHYSIONET_USERNAME")
password = os.getenv("PHYSIONET_PASSWORD")

if not username or not password:
    raise ValueError("Please set PHYSIONET_USERNAME and PHYSIONET_PASSWORD in your .env file")

base_url = "https://physionet.org/files/mimic-iv-echo/0.1/"
dicom_path = "files/p16/p16846280/s96459668/96459668_0001.dcm"
url = f"{base_url}{dicom_path}"

cmd = [
    "wget",
    "-r",
    "-N",
    "-c",
    "-np",
    "--user", username,
    "--password", password,
    "-P", "../assets",
    url
]


try:
    subprocess.run(cmd, check=True)
    print("Download complete")
except subprocess.CalledProcessError as e:
    print(f"Failure: {e}")
