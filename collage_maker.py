from PIL import Image
import os
import math
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_jpg_files(folder_path):
    """Get all JPG files from the photos folder"""
    jpg_files = []
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.jpg', '.jpeg')):
                jpg_files.append(os.path.join(folder_path, filename))
    return jpg_files

def resize_image_keep_ratio(image, target_size):
    """Resize image while keeping aspect ratio and centering the crop"""
    # Calculate ratios
    img_ratio = image.width / image.height
    target_ratio = target_size[0] / target_size[1]
    
    if img_ratio > target_ratio:
        # Image is wider, fit by height and crop from center
        new_height = target_size[1]
        new_width = int(new_height * img_ratio)
    else:
        # Image is taller, fit by width and crop from center
        new_width = target_size[0]
        new_height = int(new_width / img_ratio)
    
    # Resize image
    resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Calculate crop box to show the CENTER of the image
    left = (new_width - target_size[0]) // 2
    top = (new_height - target_size[1]) // 2
    right = left + target_size[0]
    bottom = top + target_size[1]
    
    # Ensure we don't go outside image bounds
    left = max(0, left)
    top = max(0, top)
    right = min(new_width, right)
    bottom = min(new_height, bottom)
    
    return resized.crop((left, top, right, bottom))

def create_collage():
    """Create a full-coverage collage where all images are visible with centers preserved"""
    photos_folder = 'photos'
    jpg_files = get_jpg_files(photos_folder)
    
    if not jpg_files:
        print("Keine JPG-Dateien im photos Ordner gefunden!")
        return
    
    print(f"Gefunden: {len(jpg_files)} Bilder")
    
    # Canvas settings from environment variables
    canvas_width = int(os.getenv('COLLAGE_WIDTH', 1080))
    canvas_height = int(os.getenv('COLLAGE_HEIGHT', 1920))
    
    # Create blank canvas with dark background
    canvas = Image.new('RGB', (canvas_width, canvas_height), (20, 20, 20))
    
    # Shuffle images for random placement
    random.shuffle(jpg_files)
    
    num_images = len(jpg_files)
    
    # Calculate optimal grid based on number of images and canvas ratio
    canvas_ratio = canvas_width / canvas_height  # 1080/1920 = 0.5625
    
    # For vertical canvas, we want more rows than columns
    grid_cols = max(3, math.ceil(math.sqrt(num_images * canvas_ratio)))
    grid_rows = math.ceil(num_images / grid_cols)
    
    # Ensure we don't create too many empty cells
    while grid_cols * grid_rows > num_images * 1.5 and grid_cols > 3:
        grid_cols -= 1
        grid_rows = math.ceil(num_images / grid_cols)
    
    # Calculate cell dimensions with heavy overlap to eliminate gaps
    overlap_factor = 0.5  # 50% overlap between cells for better coverage
    
    # Calculate spacing between cell centers (smaller spacing = more overlap)
    cell_spacing_x = canvas_width / (grid_cols + 0.5)  # Tighter spacing
    cell_spacing_y = canvas_height / (grid_rows + 0.5)
    
    # Base image size - much larger to ensure no gaps
    base_image_size = max(cell_spacing_x, cell_spacing_y) * 1.4  # 40% larger than spacing
    
    print(f"Grid: {grid_rows}x{grid_cols}, Effektive Bildgröße: {base_image_size:.0f}px")
    
    # Place each image in its designated cell with controlled randomness
    for i, jpg_file in enumerate(jpg_files):
        try:
            # Load image
            img = Image.open(jpg_file)
            
            # Calculate grid position
            row = i // grid_cols
            col = i % grid_cols
            
            # Size variation around base size (larger sizes to fill gaps)
            size_variation = random.uniform(1.0, 1.4)  # All images bigger
            image_size = int(base_image_size * size_variation)
            
            # Resize image
            img = resize_image_keep_ratio(img, (image_size, image_size))
            
            # Calculate center of the cell
            cell_center_x = col * cell_spacing_x + cell_spacing_x / 2
            cell_center_y = row * cell_spacing_y + cell_spacing_y / 2
            
            # Add random offset for organic look (moderate offset to maintain coverage)
            max_offset_x = cell_spacing_x * 0.3
            max_offset_y = cell_spacing_y * 0.3
            
            offset_x = random.uniform(-max_offset_x, max_offset_x)
            offset_y = random.uniform(-max_offset_y, max_offset_y)
            
            # Final center position
            final_center_x = cell_center_x + offset_x
            final_center_y = cell_center_y + offset_y
            
            # Calculate top-left position
            x = int(final_center_x - image_size / 2)
            y = int(final_center_y - image_size / 2)
            
            # Allow images to extend beyond canvas edges to fill space
            # but ensure center remains visible
            min_visible_size = image_size // 3
            x = max(-image_size + min_visible_size, min(x, canvas_width - min_visible_size))
            y = max(-image_size + min_visible_size, min(y, canvas_height - min_visible_size))
            
            # Light rotation for artistic effect
            rotation = random.uniform(-8, 8)
            if abs(rotation) > 1:
                # Rotate around center
                img = img.rotate(rotation, expand=False, fillcolor=(20, 20, 20))
            
            # Paste image onto canvas
            canvas.paste(img, (x, y))
            
            print(f"✓ Eingefügt: {os.path.basename(jpg_file)} bei ({x}, {y}) Größe: {image_size}px Rotation: {rotation:.1f}°")
            
        except Exception as e:
            print(f"✗ Fehler bei {jpg_file}: {e}")
    
    # Always add extra layer for gap filling regardless of image count
    print("Fülle verbleibende Lücken mit zusätzlicher Schicht...")
    
    # First pass: Fill obvious gaps with medium-sized images
    gap_fill_positions = []
    
    # Create positions between main grid points
    for row in range(grid_rows + 1):
        for col in range(grid_cols + 1):
            x_pos = col * cell_spacing_x
            y_pos = row * cell_spacing_y
            
            # Add some offset positions around edges and between main positions
            positions_to_try = [
                (x_pos + cell_spacing_x * 0.5, y_pos + cell_spacing_y * 0.5),
                (x_pos + cell_spacing_x * 0.25, y_pos + cell_spacing_y * 0.75),
                (x_pos + cell_spacing_x * 0.75, y_pos + cell_spacing_y * 0.25),
            ]
            
            for px, py in positions_to_try:
                if 0 <= px <= canvas_width and 0 <= py <= canvas_height:
                    gap_fill_positions.append((px, py))
    
    # Add medium-sized gap fillers
    gap_count = min(len(gap_fill_positions), num_images // 2)
    selected_gap_positions = random.sample(gap_fill_positions, min(gap_count, len(gap_fill_positions)))
    
    for i, (x_pos, y_pos) in enumerate(selected_gap_positions):
        if i < len(jpg_files):
            try:
                img = Image.open(jpg_files[random.randint(0, len(jpg_files)-1)])
                
                # Medium size for gap filling
                gap_size = int(base_image_size * random.uniform(0.6, 0.9))
                img = resize_image_keep_ratio(img, (gap_size, gap_size))
                
                x = int(x_pos - gap_size / 2)
                y = int(y_pos - gap_size / 2)
                
                # Rotation for gap fillers
                rotation = random.uniform(-15, 15)
                if abs(rotation) > 2:
                    img = img.rotate(rotation, expand=False, fillcolor=(20, 20, 20))
                
                canvas.paste(img, (x, y))
                print(f"✓ Lückenfüller: bei ({x}, {y}) Größe: {gap_size}px")
                
            except Exception as e:
                print(f"✗ Fehler bei Lückenfüller: {e}")
    
    # Second pass: Add random scattered small images for final coverage
    if num_images > 30:
        print("Füge finale kleine Bilder für komplette Abdeckung hinzu...")
        
        # Random scattered positions across the entire canvas
        scatter_positions = []
        for _ in range(num_images):
            x_pos = random.uniform(0, canvas_width)
            y_pos = random.uniform(0, canvas_height)
            scatter_positions.append((x_pos, y_pos))
        
        # Add small scattered images
        scatter_count = min(len(scatter_positions), num_images // 4)
        
        for i in range(scatter_count):
            try:
                img = Image.open(jpg_files[random.randint(0, len(jpg_files)-1)])
                
                # Small size for scattered coverage
                scatter_size = int(base_image_size * random.uniform(0.3, 0.6))
                img = resize_image_keep_ratio(img, (scatter_size, scatter_size))
                
                x_pos, y_pos = scatter_positions[i]
                x = int(x_pos - scatter_size / 2)
                y = int(y_pos - scatter_size / 2)
                
                # High rotation for scattered images
                rotation = random.uniform(-30, 30)
                if abs(rotation) > 5:
                    img = img.rotate(rotation, expand=False, fillcolor=(20, 20, 20))
                
                canvas.paste(img, (x, y))
                print(f"✓ Streuung: bei ({x}, {y}) Größe: {scatter_size}px")
                
            except Exception as e:
                print(f"✗ Fehler bei Streuung: {e}")
    
    # Save collage
    output_path = 'album_collage.jpg'
    canvas.save(output_path, 'JPEG', quality=95)
    print(f"\n🎨 Collage gespeichert als: {output_path}")
    print(f"Größe: {canvas_width}x{canvas_height} Pixel (9:16 Hochformat)")
    print(f"Alle {num_images} Bilder wurden platziert!")

if __name__ == "__main__":
    create_collage()