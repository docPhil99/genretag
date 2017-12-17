#! /usr/bin/python
"""A simple script that changes all the genre tags (via taglib) in a directory. The tags are set via flags on the command line. Run ./GenreTag -h for help. """
import glob
import os
import sys
import taglib
import argparse

parser=argparse.ArgumentParser(description="Changes the genre tags of the music in a give directoy. If no options are given it prints the existing tags")
parser.add_argument('name',help='directory of music to change. ')
#the optional genre tags
parser.add_argument('-o','--orchestral',action='store_true')
parser.add_argument('-c','--chamber',action='store_true')
parser.add_argument('-p','--opera',action='store_true')

parser.add_argument('-f','--film',action='store_true')
parser.add_argument('-j','--jazz',action='store_true')
parser.add_argument('-r','--poprock',action='store_true')
parser.add_argument('-x','--christmas',action='store_true')
args=vars(parser.parse_args())
print(args)
newGenre=[]
for key,value in args.iteritems():
    if value:
        if key is not 'name':
            newGenre.append(key.upper())
print newGenre
extList=('*.flac','*.mp3','*.m4a')
print len(sys.argv)
path=args['name']
files=[]
for ext in extList:
    fs=os.path.join(path,ext)
    print fs
    files.append(glob.glob(fs))
flatten_files=[y for x in files for y in x]
assert len(flatten_files)>0, "No supported media files found"
for file in flatten_files:
    print('File '+file)
    song=taglib.File(file)
    print(song.tags["GENRE"])
    if len(newGenre)>0:
        song.tags["GENRE"]=newGenre
        ret=song.save()
        print(ret)
