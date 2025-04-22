from matplotlib.pyplot import subplots, close
from matplotlib.backends.backend_pdf import PdfPages
from pydicom import dcmread
from pydicom.pixel_data_handlers.util import convert_color_space

base_path = './assets/physionet.org/files/mimic-iv-echo/0.1/'


def convert_to_pdf(dicom_path: str):
    file_path = f'{base_path}{dicom_path}'
    dicom_data = dcmread(file_path)

    txt_filename = file_path.replace('.dcm', '.txt')
    with open(txt_filename, 'w') as f:
        f.write(str(dicom_data))

    images_rgb = convert_to_rgb(dicom_data.pixel_array)

    pdf_filename = file_path.replace('.dcm', '.pdf')
    with PdfPages(pdf_filename) as pdf:
        for i, img in enumerate(images_rgb):
            fig, ax = subplots(figsize=(10, 6))
            ax.imshow(img)
            ax.axis('off')
            ax.set_title(f'Frame {i + 1}')
            pdf.savefig(fig)
            close(fig)

    return pdf_filename


def convert_to_rgb(pixel_array):
    return convert_color_space(
        pixel_array,
        "YBR_FULL_422",
        "RGB",
        per_frame=True
    )
