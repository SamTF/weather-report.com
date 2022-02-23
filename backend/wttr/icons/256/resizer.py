import os
from PIL import Image

for f in os.listdir():
    if f.endswith('py'): continue
    if f == '128': continue

    print(f)
    img = Image.open(f).convert('RGBA')
    resized = img.resize((128,128))

    resized.save(f'128/{f}')
