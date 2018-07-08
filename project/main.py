import os
import os.path
import re

# import regex
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


def parse_sect_(file, file_name, bar, ctrl=None):
    while 1 == 1:
        line = file.readline().decode('utf8').strip()
        bar.update(file.tell())
        prop = re.match('(Top|Left|Height|Width|Caption)\s*=\s*\'?(.+?)\'?$', line)
        if prop:
            prop_mapper(ctrl,  prop.group(1), prop.group(2))

        if re.match('end', line):
            return

        sect = re.search('(object|inherited)\s+(\w+)\s*:\s*(\w+)', line)
        if sect:
            child = Control.create(file_name=file_name, name=sect.group(2), type=sect.group(3), parent=ctrl)
            parse_sect_(file, file_name, bar, child)


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


class Parser:
    re_sect = re.compile('(object|inherited)|(end)', re.IGNORECASE | re.DOTALL)
    re_title = re.compile('\s+(\w+)\s*:\s*(\w+)', re.IGNORECASE | re.DOTALL)
    re_prop = re.compile('(Top|Left|Height|Width|Caption)\s*=\s*(\d+|\'.+?\')', re.IGNORECASE | re.DOTALL)
    re_prop_ = re.compile('(\w+)\s*=\s*\'?(.+?)\'?', re.IGNORECASE | re.DOTALL)

    Control.create_table()

    def __init__(self, file_name, text):
        self.file_name = file_name
        self.text = text
        self.pos = 0

        self.bar = ProgressBar(maxval=os.path.getsize(self.file_name)).start()
        self.sector()
        self.bar.finish()

    def parse_prop(self, ctrl, end):
        while self.pos < end:
            prop = self.re_prop.search(self.text, self.pos, end)
            if prop:
                name = prop.group(1)
                val = prop.group(2)
                self.pos = prop.end()
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
            else:
                return

    def sector(self, ctrl=None):
        while True:
            sect = self.re_sect.search(self.text, self.pos)
            if sect:
                self.parse_prop(ctrl, sect.start())
                if sect.group(1):
                    title = self.re_title.search(self.text, sect.end())
                    child = Control.create(file_name=self.file_name, name=title.group(1), type=title.group(2), parent=ctrl)
                    self.pos = title.end()
                    self.sector(child)

                elif sect.group(2):
                    self.pos = sect.end()
                    self.bar.update(self.pos)
                    return


with open('mt400.dfm', 'rb') as f:
    text = f.read().decode('utf8')
    # re_title = re.compile('(object|inherited)\s+(\w+)\s*:\s*(\w+)', re.IGNORECASE|re.DOTALL)
    pos = 0
    parser = Parser('mt400.dfm', text)


    # while True:
    #     res = re_sect.search(text, pos)
    #     if res:
    #         if
    #         print(res.group(4))
    #         pos = res.end()
    #     else:
    #         break


