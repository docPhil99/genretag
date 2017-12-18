#! /usr/bin/python
"""A simple script that changes all the genre tags (via taglib) in a directory. The tags are set via flags on the command line. Run ./GenreTag -h for help. """
from __future__ import print_function    # (at top of module)

import glob
import os
import sys
import taglib
import argparse
#import fnmatch
import re
parser=argparse.ArgumentParser(description="Changes the genre tags of the music in a give directoy. If no options are given it prints the existing tags")
parser.add_argument('name',help='directory of music to change. ')
#the optional genre tags
parser.add_argument('-R','--recursive',action='store_true',help="Recursively search directories")

parser.add_argument('-o','--Orchestral',action='store_true')
parser.add_argument('-c','--Chamber',action='store_true')
parser.add_argument('-p','--Opera',action='store_true')
parser.add_argument('-ch','--Choral',action='store_true')
parser.add_argument('-pi','--Piano',action='store_true')
parser.add_argument('-s','--Soundtrack',action='store_true')
parser.add_argument('-j','--Jazz',action='store_true')
parser.add_argument('-r','--PopRock',action='store_true')
parser.add_argument('-x','--Christmas',action='store_true')
parser.add_argument('-m','--Minimalist',action='store_true')
parser.add_argument('-E','--Early',action='store_true')
parser.add_argument('-B','--Baroque',action='store_true')
parser.add_argument('-RO','--Romantic',action='store_true')
parser.add_argument('-C','--Classical',action='store_true')
parser.add_argument('-N','--Nationalistic',action='store_true')
parser.add_argument('-MO','--Modern',action='store_true')
parser.add_argument('--Misc',action='store_true')

args=vars(parser.parse_args())
print(args)
newGenre=[]
for key,value in args.iteritems():
    if value:
        if key is not 'name' and key is not 'recursive':
            newGenre.append(key)
print(newGenre)
#extList=('.flac','.mp3','.m4a','.aiff')
re_extList='.flac$|.mp3$|.m4a$|.aiff$'
path=args['name']
files=[]
if not args['recursive']:
    print("Scanning...")
    for filename in os.listdir(path):
        if bool(re.search(re_extList,filename,re.I)):
            files.append(os.path.join(path,filename))
#    for ext in extList:
#        fs=os.path.join(path,'*'+ext)
#        print(fs)
#        files.append(glob.glob(fs))
#        flatten_files=[y for x in files for y in x]

else:
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if bool(re.search(re_extList,filename,re.I)):
                files.append(os.path.join(root, filename))
flatten_files=files
#assert len(flatten_files)>0, "No supported media files found"
if len(flatten_files)==0:
    sys.exit("No supported media file found")
for file in flatten_files:
    print('File '+file)
    try:
        song=taglib.File(file)
    except:
        print("Could not read file")
        continue
    
    if "GENRE" in song.tags.keys():
         print(song.tags["GENRE"])
    else:
         print("No tag")
    if len(newGenre)>0:
        try:
            song.tags["GENRE"]=newGenre
            ret=song.save()
            print("Set to new genre ")
            print(', '.join(newGenre))
        except:
            print("Could not save file!")
