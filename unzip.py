import zipfile

with zipfile.ZipFile("A Journey of Black and Red.zip", 'r') as epub:
    folder = "unziped"
    epub.extractall(folder)