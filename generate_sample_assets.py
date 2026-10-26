"""Generate clean sample benchmark images for demonstration and offline testing."""
import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("assets", exist_ok=True)

def create_ppe_compliant_image():
    img = Image.new("RGB", (800, 600), color=(210, 220, 230))
    draw = ImageDraw.Draw(img)
    
    # Background building frame / concrete slab
    draw.rectangle([0, 420, 800, 600], fill=(130, 135, 140)) # ground / slab
    draw.rectangle([60, 100, 160, 420], fill=(170, 175, 180)) # column 1
    draw.rectangle([640, 100, 740, 420], fill=(170, 175, 180)) # column 2
    draw.rectangle([50, 70, 750, 120], fill=(150, 155, 160)) # beam
    
    # Scaffolding pipes (yellow/steel)
    for x in range(200, 600, 80):
        draw.line([(x, 120), (x, 420)], fill=(234, 179, 8), width=5)
    for y in range(160, 420, 70):
        draw.line([(180, y), (620, y)], fill=(234, 179, 8), width=4)
        
    # Worker 1: Fully Compliant
    # Yellow Hardhat
    draw.ellipse([320, 200, 360, 235], fill=(250, 204, 21)) # Yellow Helmet
    draw.arc([315, 220, 365, 240], 0, 180, fill=(200, 150, 10), width=4)
    # Head / Face
    draw.ellipse([325, 225, 355, 255], fill=(235, 185, 150))
    # Hi-Vis Orange Vest with reflective yellow/white stripes
    draw.rectangle([310, 255, 370, 340], fill=(249, 115, 22)) # Orange vest
    draw.line([(320, 255), (320, 340)], fill=(255, 255, 255), width=4) # stripe
    draw.line([(360, 255), (360, 340)], fill=(255, 255, 255), width=4) # stripe
    draw.line([(310, 300), (370, 300)], fill=(250, 204, 21), width=6) # waist reflective
    # Full body safety harness straps (green webbing)
    draw.line([(320, 260), (350, 320)], fill=(16, 185, 129), width=3)
    draw.line([(360, 260), (330, 320)], fill=(16, 185, 129), width=3)
    # Work Trousers
    draw.rectangle([315, 340, 338, 410], fill=(30, 41, 59))
    draw.rectangle([342, 340, 365, 410], fill=(30, 41, 59))
    # Steel toe safety boots (dark brown/black with reinforced cap)
    draw.rectangle([310, 405, 340, 422], fill=(20, 20, 20))
    draw.rectangle([340, 405, 370, 422], fill=(20, 20, 20))
    
    # Worker 2: Compliant engineer holding blueprint
    draw.ellipse([460, 210, 495, 245], fill=(255, 255, 255)) # White Engineer Helmet
    draw.ellipse([465, 235, 490, 260], fill=(225, 175, 140))
    draw.rectangle([450, 260, 505, 340], fill=(234, 88, 12)) # Fluorescent vest
    draw.line([(450, 300), (505, 300)], fill=(255, 255, 255), width=5)
    draw.rectangle([455, 340, 475, 410], fill=(51, 65, 85))
    draw.rectangle([480, 340, 500, 410], fill=(51, 65, 85))
    draw.rectangle([450, 405, 477, 422], fill=(30, 30, 30))
    draw.rectangle([478, 405, 505, 422], fill=(30, 30, 30))
    # Blueprint roll
    draw.rectangle([495, 280, 530, 300], fill=(255, 255, 255))
    
    # Site safety signage
    draw.rectangle([20, 20, 260, 65], fill=(22, 101, 52)) # Green header
    draw.text((30, 28), "SAFETY AUDIT: 100% PPE COMPLIANT", fill=(255, 255, 255))
    draw.text((30, 44), "IS 456 / OSHA 1926 VERIFIED SITE", fill=(187, 247, 208))
    
    img.save("assets/sample_ppe_compliant.jpg", quality=90)
    print("Generated sample_ppe_compliant.jpg")

def create_ppe_violation_image():
    img = Image.new("RGB", (800, 600), color=(220, 215, 210))
    draw = ImageDraw.Draw(img)
    
    # Construction Excavation / Trench & Scaffolding
    draw.rectangle([0, 380, 800, 600], fill=(120, 90, 60)) # soil / excavation
    draw.polygon([(0, 380), (350, 380), (280, 600), (0, 600)], fill=(80, 50, 30)) # deep trench
    draw.rectangle([400, 150, 430, 380], fill=(160, 160, 160)) # concrete column
    
    # Worker 1: CRITICAL VIOLATION - No helmet, regular street t-shirt, sandals/sneakers, near edge
    draw.ellipse([250, 240, 280, 275], fill=(70, 40, 20)) # Hair (NO HELMET)
    draw.ellipse([252, 250, 278, 280], fill=(225, 175, 140)) # Face
    # Regular Blue T-shirt (NO HI-VIS VEST)
    draw.rectangle([240, 280, 290, 350], fill=(37, 99, 235))
    # Trousers
    draw.rectangle([245, 350, 265, 410], fill=(100, 116, 139))
    draw.rectangle([270, 350, 290, 410], fill=(100, 116, 139))
    # Slippers / Open footwear (NO SAFETY BOOTS)
    draw.rectangle([240, 408, 265, 418], fill=(239, 68, 68)) # red sandals
    draw.rectangle([270, 408, 295, 418], fill=(239, 68, 68))
    
    # Worker 2: Elevated on beam with NO SAFETY HARNESS
    draw.line([(380, 180), (750, 180)], fill=(140, 140, 150), width=15) # steel beam
    draw.ellipse([550, 110, 580, 140], fill=(250, 204, 21)) # has helmet
    draw.ellipse([555, 130, 575, 150], fill=(225, 175, 140))
    draw.rectangle([545, 150, 585, 200], fill=(249, 115, 22)) # has vest
    # But working at 6m height with NO fall arrest lanyard attached to lifeline!
    draw.line([(550, 200), (550, 230)], fill=(30, 41, 59), width=8)
    draw.line([(575, 200), (575, 230)], fill=(30, 41, 59), width=8)
    
    # Hazard Alert Callouts
    draw.rectangle([20, 20, 300, 65], fill=(185, 28, 28)) # Red header
    draw.text((30, 28), "HAZARDS DETECTED: HIGH RISK", fill=(255, 255, 255))
    draw.text((30, 44), "UNPROTECTED TRENCH & MISSING PPE", fill=(254, 202, 202))
    
    img.save("assets/sample_ppe_violation.jpg", quality=90)
    print("Generated sample_ppe_violation.jpg")

def create_crack_shear_image():
    img = Image.new("RGB", (800, 600), color=(185, 188, 192)) # concrete texture base
    draw = ImageDraw.Draw(img)
    
    # Concrete beam & column junction
    draw.rectangle([0, 0, 800, 600], fill=(180, 184, 188))
    # Formwork joint line
    draw.line([(0, 200), (800, 200)], fill=(160, 164, 168), width=3)
    
    # Severe 45° Diagonal Structural Shear Crack with branches
    crack_points = [
        (120, 520), (160, 480), (210, 440), (250, 390), (310, 350), 
        (370, 300), (420, 270), (480, 220), (540, 180), (600, 130), 
        (660, 90), (710, 60)
    ]
    # Draw crack outer halo (shadow / spall edge)
    for i in range(len(crack_points)-1):
        draw.line([crack_points[i], crack_points[i+1]], fill=(70, 72, 75), width=9)
    # Draw dark inner fracture void (6.5mm)
    for i in range(len(crack_points)-1):
        draw.line([crack_points[i], crack_points[i+1]], fill=(25, 25, 28), width=5)
        
    # Micro branching cracks
    draw.line([(310, 350), (350, 370), (380, 410)], fill=(40, 40, 42), width=3)
    draw.line([(480, 220), (460, 180), (450, 140)], fill=(40, 40, 42), width=3)
    
    # Spalling area near crack zone (concrete flaking revealing rust)
    draw.ellipse([340, 310, 390, 350], fill=(130, 100, 80)) # rust stained spall
    draw.rectangle([355, 325, 380, 335], fill=(110, 60, 30)) # exposed rebar section
    
    # Inspection scale / ruler marker
    draw.rectangle([680, 450, 770, 570], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw.text((690, 460), "INSPECTION", fill=(0, 0, 0))
    draw.text((690, 480), "SCALE (mm)", fill=(0, 0, 0))
    for tick in range(500, 560, 10):
        draw.line([(680, tick), (710, tick)], fill=(0, 0, 0), width=2)
    draw.text((715, 520), "6.5 mm", fill=(220, 38, 38))
    
    # Defect badge
    draw.rectangle([20, 20, 320, 65], fill=(153, 27, 27))
    draw.text((30, 28), "CRACK DEFECT: STRUCTURAL SHEAR", fill=(255, 255, 255))
    draw.text((30, 44), "IS 456 CL. 40 / IMMEDIATE REPAIR REQ.", fill=(254, 202, 202))
    
    img.save("assets/sample_crack_shear.jpg", quality=90)
    print("Generated sample_crack_shear.jpg")

def create_crack_hairline_image():
    img = Image.new("RGB", (800, 600), color=(235, 232, 225)) # painted plaster wall
    draw = ImageDraw.Draw(img)
    
    # Plaster stipple texture subtle lines
    for y in range(0, 600, 40):
        draw.line([(0, y), (800, y)], fill=(230, 227, 220), width=1)
        
    # Hairline crack (meandering fine line < 0.4 mm)
    fine_crack = [
        (250, 80), (270, 120), (265, 170), (290, 220), (280, 270),
        (300, 320), (320, 380), (315, 430), (330, 480), (340, 530)
    ]
    for i in range(len(fine_crack)-1):
        draw.line([fine_crack[i], fine_crack[i+1]], fill=(140, 135, 130), width=2)
    for i in range(len(fine_crack)-1):
        draw.line([fine_crack[i], fine_crack[i+1]], fill=(90, 85, 80), width=1)
        
    # Inspection scale
    draw.rectangle([680, 450, 770, 570], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw.text((690, 460), "INSPECTION", fill=(0, 0, 0))
    draw.text((690, 480), "SCALE (mm)", fill=(0, 0, 0))
    draw.text((715, 520), "0.3 mm", fill=(202, 138, 4))
    
    draw.rectangle([20, 20, 320, 65], fill=(30, 64, 175))
    draw.text((30, 28), "CRACK DEFECT: HAIRLINE SHRINKAGE", fill=(255, 255, 255))
    draw.text((30, 44), "NON-STRUCTURAL / MONITORING ONLY", fill=(191, 219, 254))
    
    img.save("assets/sample_crack_hairline.jpg", quality=90)
    print("Generated sample_crack_hairline.jpg")

if __name__ == "__main__":
    create_ppe_compliant_image()
    create_ppe_violation_image()
    create_crack_shear_image()
    create_crack_hairline_image()
