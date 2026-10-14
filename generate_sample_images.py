"""
Generate realistic civic sample images for CivicLens AI
Produces Before & After images for potholes, garbage dumps, live wire hazards, and waterlogging.
"""
import os
from PIL import Image, ImageDraw

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "static", "sample_images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_base(width=800, height=500, bg_color=(80, 80, 85)):
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    return img, draw

def save_image(img, filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath, "JPEG", quality=90)
    print(f"Generated {filepath}")

# 1. Pothole Before (Cratered road)
def gen_pothole_before():
    img, draw = create_base(800, 500, (65, 68, 72)) # Asphalt gray
    # Road markings (faded yellow center line)
    for y in range(0, 500, 80):
        draw.rectangle([390, y, 410, y + 45], fill=(210, 190, 80))
    # Curbs and roadside
    draw.rectangle([0, 0, 80, 500], fill=(130, 125, 115))
    draw.rectangle([720, 0, 800, 500], fill=(130, 125, 115))
    
    # Large jagged crater / pothole
    crater_coords = [
        (310, 220), (370, 190), (460, 210), (510, 260), 
        (490, 340), (430, 370), (340, 360), (280, 300), (300, 250)
    ]
    draw.polygon(crater_coords, fill=(28, 26, 25)) # Deep dark asphalt base
    for offset in range(1, 15):
        draw.polygon([(x - offset, y - offset) for x, y in crater_coords[::2]], outline=(15, 15, 15), width=2)
    # Radiating cracks
    cracks = [
        [(310, 220), (240, 180), (210, 190)],
        [(510, 260), (580, 280), (630, 260)],
        [(430, 370), (450, 440), (430, 470)],
        [(340, 360), (290, 410), (270, 450)]
    ]
    for crack in cracks:
        draw.line(crack, fill=(20, 20, 20), width=3)
        draw.line(crack, fill=(45, 45, 45), width=1)
        
    # Gravel and loose stones around crater
    import random
    random.seed(42)
    for _ in range(60):
        gx = random.randint(260, 540)
        gy = random.randint(180, 390)
        r = random.randint(2, 6)
        draw.ellipse([gx, gy, gx + r, gy + r], fill=(140, 135, 130))
        
    # Water reflection in pothole
    draw.ellipse([340, 260, 450, 320], fill=(45, 55, 60))
    save_image(img, "pothole_before.jpg")

# 2. Pothole After (Repaired smooth asphalt patch)
def gen_pothole_after():
    img, draw = create_base(800, 500, (65, 68, 72))
    for y in range(0, 500, 80):
        draw.rectangle([390, y, 410, y + 45], fill=(210, 190, 80))
    draw.rectangle([0, 0, 80, 500], fill=(130, 125, 115))
    draw.rectangle([720, 0, 800, 500], fill=(130, 125, 115))
    
    # Freshly rolled bituminous asphalt patch
    draw.rounded_rectangle([270, 190, 530, 380], radius=25, fill=(38, 40, 44), outline=(50, 52, 58), width=3)
    draw.rounded_rectangle([268, 188, 532, 382], radius=27, outline=(25, 25, 28), width=4)
    for x in range(290, 510, 25):
        draw.line([(x, 205), (x, 365)], fill=(48, 50, 55), width=2)
    save_image(img, "pothole_after.jpg")

# 3. Garbage Dump Before
def gen_garbage_before():
    img, draw = create_base(800, 500, (110, 112, 115))
    # Brick wall
    draw.rectangle([0, 0, 800, 180], fill=(160, 105, 80))
    for y in range(0, 180, 20):
        draw.line([(0, y), (800, y)], fill=(120, 75, 55), width=1)
    draw.rectangle([0, 180, 800, 250], fill=(145, 145, 140))
    draw.line([(0, 250), (800, 250)], fill=(70, 70, 70), width=4)
    
    # Overflowing garbage mound
    import random
    random.seed(99)
    colors = [
        (220, 40, 40), (40, 140, 210), (230, 210, 30), 
        (50, 180, 70), (240, 240, 240), (30, 30, 30), (160, 110, 60)
    ]
    draw.ellipse([180, 220, 640, 460], fill=(90, 75, 60))
    for _ in range(120):
        bx = random.randint(200, 600)
        by = random.randint(230, 430)
        bw = random.randint(18, 55)
        bh = random.randint(14, 40)
        c = random.choice(colors)
        shape = random.choice(["rect", "poly", "ellipse"])
        if shape == "rect":
            draw.rectangle([bx, by, bx + bw, by + bh], fill=c, outline=(40, 40, 40))
        elif shape == "poly":
            draw.polygon([(bx, by), (bx + bw, by + 10), (bx + bw - 10, by + bh), (bx - 5, by + bh - 5)], fill=c)
        else:
            draw.ellipse([bx, by, bx + bw, by + bh], fill=c)
    draw.ellipse([150, 360, 300, 470], fill=(60, 50, 40))
    save_image(img, "garbage_before.jpg")

# 4. Garbage Dump After
def gen_garbage_after():
    img, draw = create_base(800, 500, (110, 112, 115))
    draw.rectangle([0, 0, 800, 180], fill=(175, 115, 90))
    for y in range(0, 180, 20):
        draw.line([(0, y), (800, y)], fill=(135, 85, 65), width=1)
    draw.rectangle([0, 180, 800, 250], fill=(160, 160, 155))
    draw.line([(0, 250), (800, 250)], fill=(70, 70, 70), width=4)
    draw.rectangle([0, 254, 800, 500], fill=(85, 88, 92))
    
    # Modern Swachh Bharat segregated dustbins installed
    draw.rounded_rectangle([300, 210, 380, 360], radius=8, fill=(35, 140, 50), outline=(20, 80, 30), width=3)
    draw.rectangle([310, 200, 370, 215], fill=(30, 120, 40))
    draw.rounded_rectangle([420, 210, 500, 360], radius=8, fill=(25, 110, 190), outline=(15, 60, 120), width=3)
    draw.rectangle([430, 200, 490, 215], fill=(20, 95, 165))
    save_image(img, "garbage_after.jpg")

# 5. Wire Hazard Before
def gen_wire_before():
    img, draw = create_base(800, 500, (140, 175, 205))
    draw.rectangle([0, 350, 800, 500], fill=(115, 118, 120))
    draw.rectangle([120, 60, 160, 450], fill=(85, 90, 95))
    draw.rectangle([100, 100, 180, 115], fill=(55, 60, 65))
    draw.rectangle([100, 160, 180, 175], fill=(55, 60, 65))
    
    draw.line([(140, 105), (320, 160), (450, 320), (470, 410)], fill=(20, 20, 20), width=5)
    draw.line([(140, 165), (280, 240), (390, 360), (410, 420)], fill=(180, 30, 25), width=4)
    draw.line([(140, 110), (500, 140), (800, 160)], fill=(20, 20, 20), width=4)
    draw.ellipse([460, 400, 485, 425], fill=(255, 240, 120), outline=(255, 100, 0), width=2)
    save_image(img, "wire_hazard_before.jpg")

# 6. Wire Hazard After
def gen_wire_after():
    img, draw = create_base(800, 500, (140, 175, 205))
    draw.rectangle([0, 350, 800, 500], fill=(115, 118, 120))
    draw.rectangle([120, 60, 160, 450], fill=(85, 90, 95))
    draw.rectangle([100, 100, 180, 115], fill=(55, 60, 65))
    draw.rectangle([100, 160, 180, 175], fill=(55, 60, 65))
    
    draw.line([(140, 105), (450, 110), (800, 115)], fill=(25, 25, 25), width=5)
    draw.line([(140, 165), (450, 170), (800, 175)], fill=(25, 25, 25), width=4)
    draw.rectangle([135, 180, 145, 450], fill=(220, 220, 225), outline=(50, 50, 50))
    save_image(img, "wire_hazard_after.jpg")

if __name__ == "__main__":
    gen_pothole_before()
    gen_pothole_after()
    gen_garbage_before()
    gen_garbage_after()
    gen_wire_before()
    gen_wire_after()
    print("All sample test images generated successfully.")
