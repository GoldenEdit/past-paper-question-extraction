import os
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from pdf2image import convert_from_path
import random

# Function to crop an image based on the column range and footer height
def crop_image_exclude_footer(image_path, col_range, footer_height):
    with Image.open(image_path) as img:
        img_cropped = img.crop((col_range[0], 0, col_range[1], img.height - footer_height))
    return img_cropped

# Function to perform OCR on a specific column range of an image, with the option to exclude footer
def perform_ocr_on_column_exclude_footer(image_path, col_range, footer_height, config=''):
    with Image.open(image_path) as img:
        img_cropped = img.crop((col_range[0], 0, col_range[1], img.height - footer_height))

        # Preprocessing
        # img_cropped = img_cropped.convert('L')  # Convert to grayscale
        # img_cropped = img_cropped.filter(ImageFilter.MedianFilter(size=3))  # Apply noise reduction
        # img_cropped = ImageEnhance.Contrast(img_cropped).enhance(2.0)  # Increase contrast
        # img_cropped = img_cropped.point(lambda x: 0 if x < 128 else 255, '1')  # Binarize
        rand = random.randint(1, 1000)
        #img_cropped.save(f"debug_preprocessed_image_{rand}.png")  # Save the preprocessed image for debugging

        text = pytesseract.image_to_string(img_cropped, config=config)
    return text

# Function to combine images vertically
def combine_images_vertically(image_paths):
    images = [Image.open(image_path) for image_path in image_paths]
    widths, heights = zip(*(img.size for img in images))
    total_width = max(widths)
    max_height = sum(heights)
    new_img = Image.new("RGB", (total_width, max_height), "white")
    y_offset = 0
    for img in images:
        new_img.paste(img, (0, y_offset))
        y_offset += img.height
    return new_img

# Function to process a single PDF file
def process_pdf_file(pdf_path, output_directory, paper):
    # Convert PDF to Images
    images = convert_from_path(pdf_path, first_page=2)
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_directory, f"page_{i+2}.png")
        image.save(image_path, 'PNG')
        image_paths.append(image_path)


    # OCR Configurations
    ocr_config = '--psm 6 -c tessedit_char_whitelist=123456789'
    col_range = (135, 160)
    footer_height = 200

    # Perform OCR and populate ocr_results
    ocr_results = {}
    for i, image_path in enumerate(image_paths):
        ocr_text = perform_ocr_on_column_exclude_footer(image_path, col_range, footer_height, ocr_config)
        ocr_results[f'page_{i + 2}'] = ocr_text.strip()
    

    
    buffered_pages = []
    current_question = None

    for i, image_path in enumerate(image_paths):
        page_number = i + 2
        ocr_text = ocr_results.get(f'page_{page_number}', '')

        if ocr_text.isdigit():
            detected_question = int(ocr_text)

            if current_question is None:
                current_question = detected_question

            if detected_question != current_question:
                # A new question number detected
                combined_img = combine_images_vertically(buffered_pages)
                combined_image_path = os.path.join(output_directory, f'{paper}_q_{current_question}.png')
                combined_img.save(combined_image_path)

                # Clear buffer and update current question
                buffered_pages = []
                current_question = detected_question

        if current_question is not None:
            # Add the current image path to the buffer
            buffered_pages.append(image_path)

    # Process any remaining buffered pages
    if buffered_pages:
        combined_img = combine_images_vertically(buffered_pages)
        combined_image_path = os.path.join(output_directory, f'{paper}_q_{current_question}.png')
        combined_img.save(combined_image_path)


# Function to display a simple text-based progress bar
def print_progress_bar(iteration, total, length=50):
    percent = (iteration / total)
    arrow = '=' * int(round(length * percent))
    spaces = ' ' * (length - len(arrow))
    print(f'[{arrow + spaces}] {int(percent * 100)}%', end='\r')

# Directory containing the PDF files
pdf_directory = "./past-papers"

# Loop through each PDF file in the directory
for index, pdf_filename in enumerate(os.listdir(pdf_directory)):
    if 'ms' not in pdf_filename:
        if pdf_filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, pdf_filename)
            output_directory = os.path.join("./images", pdf_filename.split('.')[0])
            main_directory = "./output"
            os.makedirs(output_directory, exist_ok=True)
            process_pdf_file(pdf_path, output_directory, pdf_filename.split('.')[0])

            # Cleanup

            # for page in enumerate(os.listdir(main_directory)):
            #     if ('page' in page):
            #         os.remove(os.path.join(main_directory, page))
            
            # Print progress bar
            print_progress_bar(index + 1, len(os.listdir(pdf_directory)))

print("\nProcessing complete.")

