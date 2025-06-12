"""
This Python file provides a basic way to test if a PDF that is loaded
into memory and modified using PyMuPDF can be sent as an attachment for
an email via Mailgun's API.
"""

import io
import os
import pymupdf

attachments_folder = os.path.abspath("mailgun/mailer/attachments")

doc1 = pymupdf.open(os.path.join(attachments_folder, "example1.pdf"))
# ...modify the PDF
pdf_bytes = doc1.write()
doc1.close()
pdf1 = io.BytesIO(pdf_bytes)

doc2 = pymupdf.open(os.path.join(attachments_folder, "example2.pdf"))
# ...modify the PDF
pdf_bytes = doc2.write()
doc2.close()
pdf2 = io.BytesIO(pdf_bytes)
