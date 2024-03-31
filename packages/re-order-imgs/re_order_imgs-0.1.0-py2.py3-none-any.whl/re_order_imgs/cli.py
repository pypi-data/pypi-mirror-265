"""Console script for re_order_imgs."""
import sys
import click
from .reorder_images_class import ReorderImages


@click.command()
@click.argument('imgs-no', type=int)
@click.option('--imgs-path',default='.',type=str,help='Path to the images you want to process')
def main(imgs_no,imgs_path):
    
    processor = ReorderImages(imgs_no,image_path=imgs_path)
    print(f"You want to process {processor.number_of_images} images and in path: {processor.image_path}")
    processor.process_images()
    return 0


if __name__ == "__main__":
    sys.exit(main())
