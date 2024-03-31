import os
import shutil
import exifread
from PIL import Image

"""Reorder images module"""
class ReorderImages:

    def __init__(self,number_of_images,image_path=None) -> None:
        self.number_of_images = number_of_images
        self.image_path = image_path
        
    
    def get_year_from_image(self,image_path):
        try:
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f)
            for tag in tags.keys():
                if tag in ('Image DateTime', 'EXIF DateTimeOriginal'):
                    date_taken = tags[tag].values
                    year = date_taken.split(':')[0]
                    return year
        except Exception as e:
            print(f"Error reading image metadata for {self.image_path}: {e}")
        return "Unknown"

    def process_images(self):
        processed_count = 0
        for root, dirs, files in os.walk(self.image_path):
            for file in files:
                if processed_count >= self.number_of_images:
                    return
                if file.lower().endswith(('jpg', 'jpeg', 'png', 'tiff', 'bmp')):
                    full_path = os.path.join(root, file)
                    year = self.get_year_from_image(full_path)
                    # Adjust the destination directory based on the year availability
                    destination_dir = os.path.join(self.image_path, year if year != "Unknown" else "unknown_years")
                    if not os.path.exists(destination_dir):
                        os.makedirs(destination_dir)
                    shutil.move(full_path, os.path.join(destination_dir, file))
                    print(f"Processed {file} into {destination_dir}")
                    processed_count += 1