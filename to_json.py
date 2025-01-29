import os
import uuid
import json
import shutil

def main():
    images = []
    for img in os.listdir('imgs'):
        images.append('imgs/' + img)

    images_formated = []
    images_name = []
    for image in images:
        name = image.split(' - ')[0]
        if name not in images_name:
            images_name.append(name)

    for image in images_name:
        names = []
        for i in (14,25,40,50,100,110):
            names.append(
                f'{image} - {i}.jpg'
            )
        images_formated.append(names)

    with open("data.json", "w") as data:
        json.dump(images_formated, data)

if __name__ == '__main__':
    main()

