from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import glob
import os


class ForeFax:
    def __init__(self, gecko_path):
        # Configure Firefox to run headless
        self.firefox_options = Options()
        self.firefox_options.headless = True

        # Create a web driver (headless browser)
        self.driver = webdriver.Firefox(options=self.firefox_options, executable_path=gecko_path)

    def load_webpage(self, pokemon):
        # Load the pokemon page with javascript
        self.driver.get(f"https://www.pokemon.com/us/pokedex/{pokemon}")

        return self.driver.page_source

    def cleanup(self):
        self.driver.quit()


def get_alts(web_page, pokemon):
    soup = BeautifulSoup(web_page, "html.parser")

    # Find the profile images div
    profile_images = soup.find("div", {"class": "profile-images"})

    # Find the actual images
    images = profile_images.find_all("img")

    # Add the alts to a list
    alts = []
    for i in range(len(images)):
        alt = (images[i])["alt"]

        # Format the alts before we add them to the list
        # Also, skip any specials which we don't need
        # (Only some are included in pokecord)
        if alt == "Alola Form":
            alt = f"Alolan {pokemon}"
        elif alt == "Galarian Form":
            alt = f"Galarian {pokemon}"
        elif alt[:4] == "Mega":
            # In this case the alt is already correct so we don't need to do anything
            pass
        else:
            continue

        # Tuple: (Special # corresponding to image file, Name of special form)
        alts.append((i + 1, alt))

    # Return immutable collection of formatted alts
    return tuple(alts)


def get_base_names(folder):
    names = []
    for imagePath in glob.iglob(f"{folder}/*.png"):
        # Get the name of the pokemon from the image
        pokemon = imagePath[imagePath.find("\\") + 1:imagePath.find("_")]

        # If the pokemon has already been recorded, skip
        if pokemon in names:
            continue

        # Add names to list of pokemon with special forms
        names.append(pokemon)

    # Return an immutable tuple with all base names of pokemon with special forms
    return tuple(names)
        

my_browser = ForeFax("C:\\Users\\Unfou\\Downloads\\geckodriver-v0.26.0-win64\\geckodriver.exe")

base_names = get_base_names("Specials")

for pokemon in base_names:
    alts = get_alts(my_browser.load_webpage(pokemon), pokemon)

    # If there are no pokecord compatible forms, skip
    if len(alts) == 0:
        continue

    # Rename image file with appropriate name
    for alt in alts:
        os.rename(f"Specials/{pokemon}_{alt[0]}.png", f"Pokemon/{alt[1]}.png")

my_browser.cleanup()
