import numpy as np
from PIL import Image

def apply_lut(image_path, lut_path, intensity=1.0):
    """
    Apply a LUT to an image
    
    Parameters:
    - image_path: Path to the source image
    - lut_path: Path to the .cube LUT file
    - intensity: Blending intensity (0.0 to 1.0)
    
    Returns:
    PIL Image with LUT applied
    """
    # Open the original image
    original_image = Image.open(image_path)
    
    # Read the LUT
    lut_data = parse_cube_lut(lut_path)
    
    # Convert image to numpy array
    img_array = np.array(original_image)
    
    # Apply LUT
    lut_result = apply_lut_to_array(img_array, lut_data)
    
    # Blend original and LUT-processed image
    blended = Image.fromarray(
        (img_array * (1 - intensity) + lut_result * intensity).astype(np.uint8)
    )
    
    return blended

def parse_cube_lut(lut_path):
    """
    Parse a .cube LUT file
    
    Returns a numpy array representing the LUT
    """
    lut = np.zeros((256, 256, 256, 3), dtype=np.uint8)
    
    with open(lut_path, 'r') as f:
        lines = f.readlines()
        lut_lines = [line.strip().split() for line in lines if line[0].isdigit()]
        
        for line in lut_lines:
            r, g, b = map(float, line)
            r_index = int(r * 255)
            g_index = int(g * 255)
            b_index = int(b * 255)
            lut[r_index, g_index, b_index] = [r_index, g_index, b_index]
    
    return lut

def apply_lut_to_array(img_array, lut_data):
    """
    Apply LUT to a numpy image array
    """
    h, w, c = img_array.shape
    result = np.zeros_like(img_array)
    
    for i in range(h):
        for j in range(w):
            r, g, b = img_array[i, j]
            result[i, j] = lut_data[r, g, b]
    
    return result

# Example usage
# result = apply_lut('input.jpg', 'color_grading.cube', intensity=0.8)
# result.save('output.jpg')
