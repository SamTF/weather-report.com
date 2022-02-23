import os

for f in os.listdir():
    if f.endswith('.py'): continue

    filename = f.replace('-01','')

    print(filename)
    os.rename(f, filename)
