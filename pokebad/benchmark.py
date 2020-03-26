from PIL import Image
import imagehash


def hash_8():
    image = Image.open("Pokemon/006_Charizard.png")
    h = str(imagehash.dhash(image, 8))


def hash_16():
    image = Image.open("Pokemon/006_Charizard.png")
    h = str(imagehash.dhash(image, 16))


if __name__ == "__main__":
    import timeit
    print(timeit.timeit("hash_8()", setup="from __main__ import hash_8", number=100000))

    print(timeit.timeit("hash_16()", setup="from __main__ import hash_16", number=100000))

    # RESULTS
    # 568.7626185
    # 521.2458809999999
    # Why is 16 bits faster? I have no idea lol
