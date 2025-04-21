import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pydicom
from pydicom.pixel_data_handlers.util import convert_color_space

# Load the DICOM file
file_path = '../../../assets/physionet.org/files/mimic-iv-echo/0.1/files/p16/p16846280/s96459668/96459668_0001.dcm'
dicom_data = pydicom.dcmread(file_path)

print("Patient ID:", dicom_data.get("PatientID"))
print("Study Date:", dicom_data.get("StudyDate"))
print("Modality:", dicom_data.get("Modality"))
print("Photometric Interpretation:", dicom_data.PhotometricInterpretation)
print(dicom_data)

# Convert YBR to RGB
images_rgb = convert_color_space(dicom_data.pixel_array, "YBR_FULL_422", "RGB", per_frame=True)

# Save all frames to a PDF
pdf_filename = "dicom_frames_output_2.pdf"
with PdfPages(pdf_filename) as pdf:
    for i, img in enumerate(images_rgb):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(img)
        ax.axis('off')
        ax.set_title(f'Frame {i + 1}')
        pdf.savefig(fig)
        plt.close(fig)

print(f"Saved {len(images_rgb)} frames to {pdf_filename}")
