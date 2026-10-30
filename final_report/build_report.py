"""Generate Complete Academic B.Tech Report for Flipkart Product Price Analysis
Outputs:
1. final_report/Flipkart_Product_Price_Analysis_Report.docx
2. final_report/Flipkart_Product_Price_Analysis_Report.pdf
"""

import os
import sys
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas

FIGURES_DIR = Path("reports/figures")
FINAL_DIR = Path("final_report")
FINAL_DIR.mkdir(parents=True, exist_ok=True)

DOCX_PATH = FINAL_DIR / "Flipkart_Product_Price_Analysis_Report.docx"
PDF_PATH = FINAL_DIR / "Flipkart_Product_Price_Analysis_Report.pdf"

print("Starting Academic Report Generation...")
