import os
import uuid
import json
import shutil

def main():
    images = []
    for img in os.listdir('imgs'):
        images.append('imgs/' + img)

    images_name = []
    images_formated = {str(i): [] for i in (14,25,40,50,100,110)}
    for image in images:
        name,size = image.split(' - ')
        size_number, extension = os.path.splitext(size)
        images_formated[size_number].append(image)

    with open('data.json', 'w') as file:
        json.dump(images_formated, file)

if __name__ == '__main__':
    main()

