import os 
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO , format = '[%(asctime)s]: %(message)s')

list_of_files =[
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "setup.py",
    "app.py",
    "research/trials.ipynb",
]

# code dh bsm  by3ml eh ?
# bycheck 3la kol folder wfile 3ndk wby4of lw folder mwgoda wla l2a wb3dha by4of lw file mwgod aw m4 mktob feh 
# lw mwgod aw mktob feh by3mlo skip lw m4 mwgod by3mlo create empty file
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir , filename = os.path.split(filepath)

    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file :{filename}")
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass
        logging.info(f"Creating empty file: {filename}")
    else:
        logging.info(f"File {filename} already exists and is not empty.")

