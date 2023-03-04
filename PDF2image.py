from pdf2image import convert_from_path, convert_from_bytes
import numpy as np
def to_image(picpath,filename):
    """transform the pdf file into images"""
    images = convert_from_path(picpath,dpi=400,
                               poppler_path = r"C:\Users\WHO\poppler-0.68.0\bin",
                               fmt="jpeg",output_file=filename,
                               output_folder='./tables',paths_only=True)
    print(images)
    return images