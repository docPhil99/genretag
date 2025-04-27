import os
import sys
import taglib
import argparse
import re
import pprint
from pathlib import Path
import itertools
from loguru import logger
from dataclasses import dataclass

@dataclass
class Album:
    Track_number: int
    Disc_number: int
    path: Path
    def  __str__(self):
        return f'Disc {self.Disc_number} Track Number {self.Track_number} File: {self.path.name}'
# return a set of selected values when a string in the form:
# 1-4,6
# would return:
# 1,2,3,4,6
# as expected...

def parseIntSet(nputstr=""):
    selection = set()
    invalid = set()
    # tokens are comma seperated values
    tokens = [x.strip() for x in nputstr.split(',')]
    for i in tokens:
        if len(i) > 0:
            if i[:1] == "<":
                i = "1-%s"%(i[1:])
        try:
            # typically tokens are plain old integers
            selection.add(int(i))
        except:
            # if not, then it might be a range
            try:
                token = [int(k.strip()) for k in i.split('-')]
                if len(token) > 1:
                    token.sort()
                    # we have items seperated by a dash
                    # try to build a valid range
                    first = token[0]
                    last = token[len(token)-1]
                    for x in range(first, last+1):
                        selection.add(x)
            except:
                # not an int and not a range...
                invalid.add(i)
    # Report invalid tokens before returning valid selection
    if len(invalid) > 0:
        print("Invalid set: " + str(invalid))
    return selection
# end parseIntSet


path = Path("/home/phil/Music/Frédéric_Chopin;_Nelson_Goerner/Nocturnes")
ext_list =['*.flac','*.mp3','*.m4a','*.aiff']
file_list = list( itertools.chain.from_iterable(path.glob(pattern) for pattern in ext_list))

print(file_list)

albums  = []
for file in file_list:
    with taglib.File(file, save_on_exit=False) as song:
        track = song.tags['TRACKNUMBER']
        if len(track) > 1:
            logger.error(f"Track number: {track} has multiple values. Using first one.")
        tn = int(track[0])
        disc_number = song.tags['DISCNUMBER']
        if len(disc_number) > 1:
            logger.error(f"Disc number: {disc_number} has multiple values. Using first one.")
        dn = int(disc_number[0])

        alb = Album(tn,dn,file)
        albums.append(alb)

#sort by track number then disc
albums.sort(key=lambda a: a.Track_number)
albums.sort(key=lambda a: a.Disc_number)

for a in albums:
    print(a)

my_range =parseIntSet("<4")
disc_num = 2

albs = [ a for a in albums if a.Track_number in my_range and a.Disc_number==disc_num]
print(albs)