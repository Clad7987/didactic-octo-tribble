#from img_scraper.downloader import main as dm

# Download images
#dm()
#print("Download done!")

# Send files to ascii/src
from shutil import move
import os
#images = [ os.path.join("img_scraper", "image_scraper", "Downloads", image) for image in os.listdir(os.path.join("img_scraper", "image_scraper", "Downloads")) ]
#for image in images:
#    move(image, os.path.join("img_to_ascii_img", "src", os.path.basename(image)))
#print("Files moved!")

#img_to_ascii_path = os.path.join("img_to_ascii_img", "src")
#for folder in os.listdir(img_to_ascii_path):
#    folder_path = os.path.join(img_to_ascii_path, folder)
#    for file in os.listdir(folder_path):
#        file_path = os.path.join(folder_path, file)
#        move(file_path, os.path.join(img_to_ascii_path, file))
#print("Adjusted images!")

# Transform into ascii
from img_to_ascii_img.img_to_clr_ascii_test import convert
import os
images = [ os.path.join("img_to_ascii_img", "src", image) for image in os.listdir("img_to_ascii_img/src") ]

from queue import Queue
from threading import Thread

q = Queue()

def worker():
    while True:
        item = q.get()
        convert(item, "imgs/")
        q.task_done()

for i in range(4):
    Thread(target=worker, daemon=True).start()

for image in images:
    q.put(image)

q.join()

print("Images Converted!")

# Create Json
#from to_json import main as jm
#jm()
#print("Data generated!")

