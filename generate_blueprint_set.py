import os
from reportlab.lib.pagesizes import landscape, A3
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

BLUE = HexColor('#1a3a6e')
DARK_BLUE = HexColor('#0f2b54')
WHITE = HexColor('#ffffff')
GOLD = HexColor('#d4a843')
GRID_COLOR = HexColor('#2a5a9e')

def add_grid(c, width, height, spacing=0.5*inch):
    c.setStrokeColor(GRID_COLOR)
    c.setLineWidth(0.25)
    for x in range(0, int(width), int(spacing)):
        c.line(x, 0, x, height)
    for y in range(0, int(height), int(spacing)):
        c.line(0, y, width, y)

def make_page(c, w, h, img_path=None, img_x=None, img_y=None, img_w=None, img_h=None, caption=None, scale="1/1"):
    c.setFillColor(BLUE)
    c.rect(0, 0, w, h, 1, 0)  # fill=1, stroke=0
    c.setStrokeColor(BLUE)
    c.setLineWidth(2)
    c.rect(0.5*inch, 0.5*inch, w-1*inch, h-1*inch, 0, 1)  # fill=0, stroke=1
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.rect(0.5*inch, 0.5*inch, w-1*inch, h-1*inch, 0, 1)  # outline
    add_grid(c, w-2*inch, h-2*inch, 0.5*inch)

    if img_path:
        c.drawImage(img_path,
                     x=img_x or 0.5*inch + (w-1*inch)/2 - 3.5*inch/2,
                     y=img_y or 0.5*inch + (h-1*inch)/2 - 5*inch/2,
                     width=img_w or 3.5*inch, height=img_h or 5*inch,
                     mask='auto', preserveAspectRatio=True,
                     anchor='c')

    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(WHITE)
    c.rect(0.5*inch, 0.5*inch, w-1*inch, 0.8*inch, 1, 0)
    c.setFillColor(DARK_BLUE)
    c.drawString(0.5*inch + 0.5*inch, 0.5*inch + 0.2*inch, caption or "THE CASEORIA")

    c.setFont("Helvetica", 8)
    c.setFillColor(GOLD)
    c.drawString(0.5*inch + 0.5*inch, 0.5*inch - 0.3*inch, f"Scale: {scale}  |  Plan #: 6797  |  Sater Design Collection")

def generate_pdf():
    pdf_path = "Casoria_Blueprint_Set.pdf"
    w, h = landscape(A3)
    c = canvas.Canvas(pdf_path, pagesize=(w, h))

    # Page 1: Cover Sheet
    c.setFillColor(BLUE)
    c.rect(0, 0, w, h, 1, 0)
    c.setStrokeColor(BLUE)
    c.setLineWidth(2)
    c.rect(0.5*inch, 0.5*inch, w-1*inch, h-1*inch, 0, 1)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.rect(0.5*inch, 0.5*inch, w-1*inch, h-1*inch, 0, 1)
    add_grid(c, w-2*inch, h-2*inch, 0.5*inch)

    c.setFillColor(DARK_BLUE)
    c.rect(0.5*inch, 0.5*inch, w-1*inch, h-1*inch, 0, 0)  # outline only, no fill
    c.setStrokeColor(BLUE)
    c.setLineWidth(1)
    c.rect(0.5*inch, 0.5*inch, w-1*inch, h-1*inch, 0, 0)

    c.setFont("Helvetica-Bold", 48)
    c.setFillColor(DARK_BLUE)
    c.drawString(w/2 - 3*inch, h/2 + 2*inch, "THE CASEORIA")
    c.setFont("Helvetica", 18)
    c.drawString(w/2 - 1.5*inch, h/2 + inch, "TUSCAN COURTYARD HOUSE PLAN")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(w/2 - 0.8*inch, h/2, "Plan #6797  |  Sater Design Collection")
    c.setFont("Helvetica", 11)
    c.drawString(w/2 - 1.5*inch, h/2 - 0.5*inch, "3,777 sqft  |  4 Bedrooms  |  5 Bathrooms  |  3-Car Garage")

    c.setFont("Helvetica", 9)
    c.setFillColor(GOLD)
    c.rect(w/2 - 2*inch, h/2 - 1.5*inch, 4*inch, 0.3*inch, 1, 0)
    c.drawString(w/2 - 1.5*inch, h/2 - 1.2*inch, "Mediterranean  •  Tuscan  •  Courtyard  •  Loggia")

    c.save()

    # Page 2: Main Level Floorplan
    c2 = canvas.Canvas(pdf_path, pagesize=(w, h))
    make_page(c2, w, h, "14_main_level_floorplan_hires.jpeg",
              w/2 - 3*inch, h/2 - 2.1*inch, 6*inch, 4.2*inch,
              "MAIN LEVEL", "1/4\" = 1'-0\"")
    c2.save()

    # Page 3: Upper Level Floorplan
    c3 = canvas.Canvas(pdf_path, pagesize=(w, h))
    make_page(c3, w, h, "15_upper_level_floorplan_hires.jpeg",
              w/2 - 2.6*inch, h/2 - 1.15*inch, 5.2*inch, 2.3*inch,
              "UPPER LEVEL", "1/4\" = 1'-0\"")
    c3.save()

    # Pages 4-10: Key Photos
    photos = [
        ("01_front_elevation.jpeg", "FRONT ELEVATION"),
        ("02_courtyard_solana_1.jpeg", "COURTYARD - SOLANA"),
        ("04_courtyard_loggia.jpeg", "COURTYARD LOGGIA"),
        ("08_great_room_kitchen_1.jpeg", "GREAT ROOM & KITCHEN"),
        ("12_master_bedroom.jpeg", "MASTER BEDROOM"),
        ("13_master_bath.jpeg", "MASTER BATHROOM"),
        ("06_rear_courtyard_elevation.jpeg", "REAR ELEVATION"),
    ]

    for i, (photo, caption) in enumerate(photos):
        c = canvas.Canvas(pdf_path, pagesize=(w, h))
        make_page(c, w, h, photo,
                  w/2 - 1.75*inch, h/2 - 2.5*inch, 3.5*inch, 5*inch,
                  caption)
        c.save()

    print(f"Blueprint set generated: {pdf_path}")
    print(f"File size: {os.path.getsize(pdf_path)/1024/1024:.1f} MB")

generate_pdf()
