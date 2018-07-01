import os
import re

lst = list(filter(lambda file: re.match('mt\d+\.dfm', file), os.listdir('.')))

print(lst)


with open('mt400.dfm', 'rb') as f:
    text = f.read().decode('utf8')


