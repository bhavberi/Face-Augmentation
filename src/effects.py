# %%
import os
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

# %%
images_base_path = "../images"
save_base_path = "../results"

# %%
def gradient_blur(img):
    # Get the center of the image
    h, w, _ = img.shape
    cy, cx = h // 2, w // 2
    
    # Calculate a normalized radius for each pixel
    y_idxs, x_idxs = np.ogrid[:h, :w]
    normalized_radius = np.sqrt((x_idxs - cx)**2 + (y_idxs - cy)**2) / np.sqrt(cx**2 + cy**2)
    
    # Divide the image into eight blur levels
    blur_levels = np.clip(normalized_radius * 8, 0, 7).astype(np.int_)
    
    # Blur the image eight times with varying standard deviations
    blurred_images = [cv2.GaussianBlur(img, (0, 0), (i+1)/2) for i in range(8)]
    
    # Combine the blurred images based on the blur level of each pixel
    combined_blurred = np.zeros_like(img)
    for i in range(8):
        mask = blur_levels == i
        combined_blurred[mask] = blurred_images[i][mask]
    
    return combined_blurred


# %%
imgs = [cv2.imread(f'{images_base_path}/{i}.jpg') for i in range(1, 4)]
blurred_imgs = [gradient_blur(img) for img in imgs]
os.makedirs('{save_base_path}/gradient_blur', exist_ok=True)
for i, img in enumerate(blurred_imgs):
    cv2.imwrite(f'{save_base_path}/gradient_blur/{i+1}.jpg', img)

# %%
def vignetting(img, d=1.0):
    h, w, _ = img.shape
    cy, cx = h // 2, w // 2

    # Calculate the distance of each pixel from the center
    y_idxs, x_idxs = np.ogrid[:h, :w]
    radius = np.sqrt((x_idxs - cx)**2 + (y_idxs - cy)**2) / np.sqrt(cx**2 + cy**2)

    # Calculate the angle theta
    theta = radius / d

    # Compute the vignetting mask using cos^4(theta)
    vignette = np.cos(theta)**4
    vignette = vignette[..., np.newaxis]

    return (img*vignette).astype(np.uint8)

# %%
imgs = [cv2.imread(f'{images_base_path}/{i}.jpg') for i in range(1, 4)]
blurred_imgs = [vignetting(img) for img in imgs]
os.makedirs('{save_base_path}/vignette', exist_ok=True)
for i, img in enumerate(blurred_imgs):
    cv2.imwrite(f'{save_base_path}/vignette/{i+1}.jpg', img)

# %%
def convert_K_to_RGB(colour_temperature):
    """
    Converts from K to RGB, algorithm courtesy of 
    http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
    """
    #range check
    if colour_temperature < 1000: 
        colour_temperature = 1000
    elif colour_temperature > 40000:
        colour_temperature = 40000
    
    tmp_internal = colour_temperature / 100.0
    
    # red 
    if tmp_internal <= 66:
        red = 255
    else:
        tmp_red = 329.698727446 * math.pow(tmp_internal - 60, -0.1332047592)
        if tmp_red < 0:
            red = 0
        elif tmp_red > 255:
            red = 255
        else:
            red = tmp_red
    
    # green
    if tmp_internal <=66:
        tmp_green = 99.4708025861 * math.log(tmp_internal) - 161.1195681661
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = tmp_green
    else:
        tmp_green = 288.1221695283 * math.pow(tmp_internal - 60, -0.0755148492)
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = tmp_green
    
    # blue
    if tmp_internal >=66:
        blue = 255
    elif tmp_internal <= 19:
        blue = 0
    else:
        tmp_blue = 138.5177312231 * math.log(tmp_internal - 10) - 305.0447927307
        if tmp_blue < 0:
            blue = 0
        elif tmp_blue > 255:
            blue = 255
        else:
            blue = tmp_blue
    
    return red, green, blue

def change_color_temperature(img, temperature, alpha=0.5):
    h, w, _ = img.shape
    color = convert_K_to_RGB(temperature)
    overlay = np.ones((h, w, 3)) * color
    blended = cv2.addWeighted(img, 1 - alpha, overlay.astype(np.uint8), alpha, 0)
    return blended

# %%
imgs = [cv2.imread(f'{images_base_path}/{i}.jpg') for i in range(1, 4)]
blurred_imgs = [change_color_temperature(img, 10000) for img in imgs]
os.makedirs('{save_base_path}/color_temperature', exist_ok=True)
for i, img in enumerate(blurred_imgs):
    cv2.imwrite(f'{save_base_path}/color_temperature/{i+1}.jpg', img)


