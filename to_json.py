import os
import uuid
import json
import shutil

files = os.listdir('./img_to_ascii_img/output/image')
dirname = os.path.dirname(__file__)

for file in files:
    shutil.move(os.path.join(dirname, 'img_to_ascii_img', 'output', 'image', file), os.path.join(dirname, 'imgs', file))
    filename, extension = os.path.splitext(file)
    filename = f'{uuid.uuid4()}{extension}'
    os.rename(os.path.join(dirname, 'imgs', file), os.path.join(dirname, 'imgs', filename))

files = os.listdir('imgs')

output = []
for file in files:
    output.append(os.path.join("./imgs", file))

with open("data.json", "w") as data:
    json.dump(output, data)
