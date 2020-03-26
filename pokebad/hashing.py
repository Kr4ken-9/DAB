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


def hash_them_all(images, output):
    db = {}

    for imagePath in glob.iglob(f"{images}/*.png"):
        # load the image and compute the difference hash
        image = Image.open(imagePath)
        h = str(imagehash.dhash(image, 16))

        # extract the filename from the path and update the database  | NOTE
        # using the hash as the key and the filename append to the    | We are using rfind because some Pokemon names have Mr. in them
        # list of values                                              | Using rfind will find the .png instead of Mr.
        filename = imagePath[imagePath.find('_') + 1:imagePath.rfind('.')]
        db[h] = filename

    with open(output, 'w') as file:
        file.write(json.dumps(db, indent=4))


hash_them_all(args.images, args.output)
