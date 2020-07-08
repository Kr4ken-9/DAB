# This is a copypasta of https://realpython.com/fingerprinting-images-for-near-duplicate-detection/
# Thanks whoever wrote this
# Example Input: ./venv/scripts/python.exe pokebad/hashing.py -i pokebad/Pokemon -o pokeboisfixed.json


from PIL import Image
import imagehash
import json
import glob
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--images", required=True, help="Path to images to hash")
parser.add_argument("-o", "--output", required=True, help="Name of file to output as (json dictionary)")
args = parser.parse_args()


# New attempt at stopping DAB is doing some alpha channel fuckery to the background of images
# Turns out it doesn't work very well if we do some basic filtering
# Discussion and details here: https://github.com/Kr4ken-9/DAB/issues/62
# Stolen from here: https://github.com/JohannesBuchner/imagehash/blob/master/examples/hashimages.py#L18
def alpharemover(image):
    if image.mode != 'RGBA':
        return image
    canvas = Image.new('RGBA', image.size, (255,255,255,255))
    canvas.paste(image, mask=image)
    return canvas.convert('RGB')


def hash_them_all(images, output):
    db = {}

    for imagePath in glob.iglob(f"{images}/*.png"):
        # load the image and compute the difference hash
        image = Image.open(imagePath)
        image = alpharemover(image)
        h = str(imagehash.dhash(image, 16))

        # extract the filename from the path and update the database  | NOTE
        # using the hash as the key and the filename append to the    | We are using rfind because some Pokemon names have Mr. in them
        # list of values                                              | Using rfind will find the .png instead of Mr.
        filename = imagePath[imagePath.find('_') + 1:imagePath.rfind('.')]
        db[h] = filename

    with open(output, 'w') as file:
        file.write(json.dumps(db, indent=4))


hash_them_all(args.images, args.output)
