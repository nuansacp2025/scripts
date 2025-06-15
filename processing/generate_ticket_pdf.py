import pymupdf
from PIL import Image, ImageDraw, ImageFont
import io
import os

ASSETS_FOLDER_PATH = os.path.join(os.path.dirname(__file__), "assets")

CATEGORIES = ["catA", "catB", "catC", "vip"]
PDFS = ["tnc"]

PAGE_WIDTH, PAGE_HEIGHT = 612, 792  # letter-sized
IMG_WIDTH, IMG_HEIGHT = 1485, 1856

class TicketPDFGenerator:
    """
    Class that stores all functions related to ticket PDF generation.
    We use a class instead of regular functions so the files remain
    open and can be reused for multiple tickets.
    """

    images: dict[str, Image.Image]
    pdfs: dict[str, pymupdf.Document]


    def __init__(self):
        self.images = {}
        for cat in CATEGORIES:
            with open(f"{ASSETS_FOLDER_PATH}/categories/{cat}.png", "rb") as f:
                self.images[cat] = Image.open(io.BytesIO(f.read()))
        self.pdfs = {}
        for pdf in PDFS:
            with open(f"{ASSETS_FOLDER_PATH}/pdfs/{pdf}.pdf", "rb") as f:
                self.pdfs[pdf] = pymupdf.open(stream=f.read())


    def generate_image(self, cat: str, seat_label: str) -> io.BytesIO:
        image = self.images[cat].copy().convert("RGBA")
        draw = ImageDraw.Draw(image)

        # Draw text at center (cx, cy)
        cx, cy = (1060, 1460)
        font = ImageFont.load_default(size=80)
        color = (255, 255, 255, 255)
        text = seat_label

        # Measure bounding box of text to be written
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        position = (cx - text_width // 2, cy - text_height // 2)
        draw.text(position, text, font=font, fill=color)

        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")

        return image_bytes


    def generate_pdf(self, image_bytes: io.BytesIO) -> io.BytesIO:
        output_pdf = pymupdf.open()

        page = output_pdf.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)

        # Load the image from bytes
        image_bytes.seek(0)
        with pymupdf.open("png", image_bytes) as img:
            img_pdf_bytes = img.convert_to_pdf()
        img_pdf = pymupdf.open("pdf", img_pdf_bytes)

        # Calculate position to center the image
        img_width = 0.45 * IMG_WIDTH
        img_height = 0.45 * IMG_HEIGHT
        x = (PAGE_WIDTH - img_width) // 2
        y = (PAGE_HEIGHT - img_height) // 2

        # Insert the image into the page
        page.show_pdf_page(pymupdf.Rect(x, y, x + img_width, y + img_height), img_pdf, 0)

        tnc = self.pdfs["tnc"]
        output_pdf.insert_pdf(tnc)

        pdf_bytes = io.BytesIO()
        output_pdf.save(pdf_bytes)
        output_pdf.close()

        return pdf_bytes

    # Generates PDFs for a list of tuples (seat_label, category)
    def generate_pdfs_from_seats(self, seats: list[tuple[str, str]]) -> list[tuple[str, bytes]]:
        def generate(seat: tuple[str, str]) -> tuple[str, bytes]:
            label, cat = seat
            fname = f"{cat}_{label}.pdf"
            image_bytes = self.generate_image(cat, label)
            pdf_bytes = self.generate_pdf(image_bytes).getvalue()
            return (fname, pdf_bytes)
        return list(map(generate, seats))

"""
Usage example

gen = TicketPDFGenerator()
pdfs = gen.generate_pdfs_from_seats([
    ("A1", "catA"),
    ("A2", "vip"),
])
# To write into file:
for filename, bytes_io in pdfs:
    with open(f"{filename}.pdf", "wb") as f:
        f.write(bytes_io.getbuffer())

"""
