from PIL import Image
from io import BytesIO
import requests


def download(pId, pName):
    # Bad gammar bad life
    pName = pName.capitalize()

    # Add zeroes and use offset because dumb api has duplicates and likes zer0es
    pId = str(pId + offset).rjust(3, "0")

    # Get the image
    img = requests.get(f'https://assets.pokemon.com/assets/cms2/img/pokedex/full/{pId}.png')
    png = Image.open(BytesIO(img.content))

    # Save the image
    print('Saved ' + pName)
    png.save(f'Pokemon/{pId}_{pName}.png', format='PNG')
    return


lastname = ""
offset = 0

pokemans = requests.get('https://www.pokemon.com/us/api/pokedex/kalos').json()
for i, c in enumerate(pokemans):
    if lastname == c['name']:
        offset -= 1
        continue
    lastname = c['name']

    print('Downloading ' + c['name'])
    download(i + 1, c['name'])
