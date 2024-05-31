import fitz  # PyMuPDF
from PIL import Image, ImageOps, ImageDraw, ImageFilter
import io
import numpy as np

def read_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images

def convert_to_black_and_white(image):
    return ImageOps.grayscale(image)

def simulate_ink_running_out(image):
    np_image = np.array(image)
    height, width = np_image.shape
    gradient = np.linspace(0, 255, width)
    gradient = np.tile(gradient, (height, 1))
    ink_effect = np.minimum(np_image, gradient)
    return Image.fromarray(ink_effect.astype(np.uint8))

def simulate_unprinted_edges(image, margin=50):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    draw.rectangle([margin, margin, width - margin, height - margin], outline="black", width=margin)
    return image

def degrade_graphics(image):
    return image.filter(ImageFilter.GaussianBlur(2))

def save_as_pdf(images, output_path):
    images[0].save(output_path, save_all=True, append_images=images[1:])

def process_pdf(input_path, output_path):
    images = read_pdf(input_path)
    processed_images = []
    for img in images:
        img = convert_to_black_and_white(img)
        img = simulate_ink_running_out(img)
        img = simulate_unprinted_edges(img)
        img = degrade_graphics(img)
        processed_images.append(img)
    save_as_pdf(processed_images, output_path)

# Example usage
process_pdf("input.pdf", "output.pdf")