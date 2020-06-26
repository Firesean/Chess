import os
from PIL import Image # Image Manipulation

CDIRECTORY = os.getcwd() + "\\"  # Current Directory

class ImageManager:

    @staticmethod
    def get_background_paths():
        backgrounds = []
        for image in sorted(os.listdir(CDIRECTORY + "images")): # Get all files in images and iterate through a sorted list
            # Checks for legitimate image and includes images that end with the specific file types
            if not image.endswith(".ico") and [image.endswith(image_type) for image_type in [".tif", ".jpg", ".gif", ".png"]]:
                backgrounds.append(image)
        return backgrounds

    @staticmethod
    def get_image_name(img_path):
        image = img_path.split(".")[0]  # Grabs everything before File type / File Name
        label = ""
        for ch in list(image):
            if ch.isupper():
                ch = " " + ch
            label += ch
        return label[0].upper() + label[1:]

    @staticmethod
    def open_image(image_path):
        return Image.open(f"{CDIRECTORY}"+ "images\\" + image_path)