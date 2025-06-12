import pymupdf
from PIL import Image, ImageDraw, ImageFont
import io
import os

ASSETS_FOLDER_PATH = os.path.join(os.path.dirname(__file__), "assets")

CATEGORIES = ["catA", "catB", "catC", "vip"]
PDFS = ["tnc"]

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

        img_pdf = pymupdf.open("png", image_bytes).convert_to_pdf()
        output_pdf.insert_pdf(pymupdf.open("pdf", img_pdf))

        tnc = self.pdfs["tnc"]
        output_pdf.insert_pdf(tnc)

        pdf_bytes = io.BytesIO()
        output_pdf.save(pdf_bytes)
        output_pdf.close()

        return pdf_bytes

    # Generates PDFs for a list of tuples (seat_label, category)
    def generate_pdfs_from_seats(self, seats: list[tuple[str, str]]) -> list[tuple[str, io.BytesIO]]:
        def generate(seat: tuple[str, str]) -> tuple[str, io.BytesIO]:
            label, cat = seat
            fname = f"{cat}_{label}.pdf"
            image_bytes = self.generate_image(cat, label)
            pdf_bytes = self.generate_pdf(image_bytes)
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
