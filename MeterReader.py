import csv
from PIL import Image
import easyocr
import os
import re
from Variables import folder_path, csv_file_path


# Function to extract the date from image metadata
def extract_date_from_metadata(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        date_taken = exif_data.get(36867)  # 36867 corresponds to the DateTimeOriginal tag in EXIF data
        return date_taken
    except (AttributeError, KeyError, IndexError):
        return None

# OCR the whole image and print results for debugging
def ocr_whole_image(image_path):
    # Use easyocr to extract text
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path)
    
    # Print OCR result for debugging
    print("OCR Result:", result)
    
    return result

# Create a list to store results for each image
all_results = []

# Iterate through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        # Full path to the image file
        image_path = os.path.join(folder_path, filename)

        # Extract the date from image metadata
        date_taken = extract_date_from_metadata(image_path)

        # OCR the whole image and print results
        result = ocr_whole_image(image_path)

        # Concatenate all recognized characters from the OCR result
        extracted_text = ''.join([text_info[1] for text_info in result])

        extracted_digits = ''.join([char for char in extracted_text if char.isdigit()])

        meter_number = extracted_digits[:6]

        # Add the entry to the CSV file
        all_results.append({
            'date_taken': date_taken,
            'extracted_text': meter_number
        })

# Write the results to the CSV file
with open(csv_file_path, mode='a', newline='') as csv_file:
    fieldnames = ['date_taken', 'extracted_text']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write each result as a new row
    for result in all_results:
        writer.writerow(result)

print("Data has been written to the CSV file.")

