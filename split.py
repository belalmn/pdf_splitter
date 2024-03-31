import sys
import os
import pdf2image
import img2pdf
from PIL import Image
import tkinter as tk
from tkinter import filedialog

def split_pdf_as_imgs(file_path, output_dir, gap=5, rotation_correction=0):
    output_file_name = os.path.basename(file_path).split('.')[0] + '- Split.pdf'
    os.makedirs(output_dir, exist_ok=True)
    images = pdf2image.convert_from_path(file_path)

    new_images = []
    for i in range(0, len(images), 2):
        old_pg_1 = images[i].rotate(-90 + rotation_correction, expand=True)
        old_pg_2 = images[i+1].rotate(90 + rotation_correction, expand=True)

        pg_4 = old_pg_1.crop((0, 0, old_pg_1.width/2, old_pg_1.height))
        pg_1 = old_pg_1.crop((old_pg_1.width/2, 0, old_pg_1.width, old_pg_1.height))
        pg_2 = old_pg_2.crop((0, 0, old_pg_2.width/2, old_pg_2.height))
        pg_3 = old_pg_2.crop((old_pg_2.width/2, 0, old_pg_2.width, old_pg_2.height))

        # create a new page 1 with pg_1 and pg_2 side by side
        pg_1_2 = Image.new('RGB', (pg_1.width + gap + pg_2.width, pg_1.height))
        pg_1_2.paste(pg_1, (0, 0))
        pg_1_2.paste(pg_2, (pg_1.width + gap, 0))

        # create a new page 2 with pg_3 and pg_4 side by side
        pg_3_4 = Image.new('RGB', (pg_3.width + gap + pg_4.width, pg_3.height))
        pg_3_4.paste(pg_3, (0, 0))
        pg_3_4.paste(pg_4, (pg_3.width + gap, 0))

        new_images.extend([pg_1_2, pg_3_4])
    
    # Create temporary directory to store images
    temp_dir = os.path.join(output_dir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    # Save images to temporary directory
    files = []
    for i, img in enumerate(new_images):
        filename = os.path.join(temp_dir, f'img_{i}.jpg')
        img.save(filename, 'JPEG')
        files.append(filename)

    # Convert images to PDF
    with open(os.path.join(output_dir, output_file_name), 'wb') as f:
        f.write(img2pdf.convert(files))

    # Remove temporary directory
    for file in files:
        os.remove(file)
    os.rmdir(temp_dir)

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    files = filedialog.askopenfiles(title='Select PDF file(s)', filetypes=[('PDF files', '*.pdf')])
    print(f'Files to split: {[file.name for file in files]}')

    output_dir = filedialog.askdirectory(title='Select output directory')
    print(f'Output directory: {output_dir}')

    # Get rotation correction argument
    rotation_correction = 0
    if input('Do you want to correct the rotation of the images? (y/n) ').lower() == 'y':
        rotation_correction = int(input('Enter the rotation correction angle (in degrees): '))

    # Split the file (or files) into images
    for file in files:
        split_pdf_as_imgs(file.name, output_dir, rotation_correction=rotation_correction)
        print(f'Successfully split {file.name} into images')