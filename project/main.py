import os
import os.path
import re

import regex
from peewee import *
from progressbar import ProgressBar

db = SqliteDatabase('controls.db')


class Control(Model):
    file_name = CharField()
    name = CharField()
    type = CharField()
    left = IntegerField(null=True)
    top = IntegerField(null=True)
    height = IntegerField(null=True)
    width = IntegerField(null=True)
    caption = CharField(null=True)
    parent = ForeignKeyField('self', backref='children', null=True)

    class Meta:
        database = db


def prop_mapper(ctrl, name, val):
    if name == 'Top':
        ctrl.top = val
    elif name == 'Left':
        ctrl.left = val
    elif name == 'Height':
        ctrl.height = val
    elif name == 'Width':
        ctrl.width = val
    elif name == 'Caption':
        ctrl.caption = val
    else:
        return

    ctrl.save()


def parse_sect(file, file_name, bar, ctrl=None):
    while 1 == 1:
        line = file.readline().decode('utf8').strip()
        bar.update(file.tell())
        prop = re.match('(Top|Left|Height|Width|Caption)\s*=\s*\'?(\d+)\'?', line)
        if prop:
            prop_mapper(ctrl,  prop.group(1), prop.group(2))

        if re.match('end', line):
            return

        sect = re.search('(object|inherited)\s+(\w+)\s*:\s*(\w+)', line)
        if sect:
            child = Control.create(file_name=file_name, name=sect.group(2), type=sect.group(3), parent=ctrl)
            parse_sect(file, file_name, bar, child)


Control.create_table()

# for fname in list(filter(lambda f: re.match('mt\d+\.dfm', f), os.listdir('.'))):
#     print(fname)
#     with open(fname, 'rb') as f:
#         bar = ProgressBar(maxval=os.path.getsize(fname)).start()
#         parse_sect(f, fname, bar)
#     bar.finish()

    # print(text)

# with open('mt400-1.txt', 'rb') as f:
#     text = f.read().decode('utf8')
#     res = regex.search('\(([^()]+|(?R))*\)', '(12asda3(aasd(aasdasdasd(dasd)sd)ss))')
#     # res = regex.search('(object|inherited)\s+(\w+)\s*:\s*(\w+).*(?R)end', text, re.IGNORECASE|re.DOTALL|re.DEBUG)
#     # res = re.search('(object|inherited)\s+(\w+):\s+(\w+)(\s+(\w+ = \w+))*end', text)
#     # print(res.groups())
#     print(res[0])
#     print(res[1])

with open('mt400.dfm', 'rb') as f:
    text = f.read().decode('utf8')
    re_title = re.compile('(object|inherited)\s+(\w+)\s*:\s*(\w+)(.*?)end', re.IGNORECASE|re.DOTALL)
    pos = 0
    while True:
        res = re_title.search(text, pos)
        if res:
            print(res.group(4))
            pos = res.end()
        else:
            break


