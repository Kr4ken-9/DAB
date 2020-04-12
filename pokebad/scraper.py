from PIL import Image
from io import BytesIO
import requests


def get_and_save(file_name, saved_name, folder="Pokemon"):
    # Get the image
    img = requests.get(f'https://assets.pokemon.com/assets/cms2/img/pokedex/full/{file_name}.png')

    # If the image does not exit, ABORT!
    # This is mostly for downloading specials
    if img.status_code == 404:
        return False

    png = Image.open(BytesIO(img.content))

    # Save the image
    print(f"Saved {saved_name}")
    png.save(f'{folder}/{saved_name}.png', format='PNG')

    return True


def download_specials(pId, pName):
    # There are different numbers of specials, so I prefer a while loop to a for loop
    # It will seem redundant to keep a variable but oh well

    special = 2
    while get_and_save(f"{pId}_f{special}", f"{pName}_{special}", "Specials"):
        special += 1


def download(pId, pName):
    # Bad gammar bad life
    pName = pName.capitalize()

    # Add zeroes and use offset because dumb api has duplicates and likes zer0es
    pId = str(pId + offset).rjust(3, "0")

    # Download and save the pokemons to PNG files
    get_and_save(pId, f"{pId}_{pName}")
    download_specials(pId, pName)
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
