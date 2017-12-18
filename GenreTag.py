#! /usr/bin/python
"""A simple script that changes all the genre tags (via taglib) in a directory. The tags are set via flags on the command line. Run ./GenreTag -h for help. """
from __future__ import print_function    # (at top of module)

import glob
import os
import sys
import taglib
import argparse
import fnmatch
parser=argparse.ArgumentParser(description="Changes the genre tags of the music in a give directoy. If no options are given it prints the existing tags")
parser.add_argument('name',help='directory of music to change. ')
#the optional genre tags
parser.add_argument('-R','--recursive',action='store_true',help="Recursively search directories")

parser.add_argument('-o','--orchestral',action='store_true')
parser.add_argument('-c','--chamber',action='store_true')
parser.add_argument('-p','--opera',action='store_true')
parser.add_argument('-ch','--choral',action='store_true')
parser.add_argument('-pi','--paino',action='store_true')
parser.add_argument('-s','--soundtrack',action='store_true')
parser.add_argument('-j','--jazz',action='store_true')
parser.add_argument('-r','--poprock',action='store_true')
parser.add_argument('-x','--christmas',action='store_true')
parser.add_argument('-m','--minimalist',action='store_true')
parser.add_argument('-E','--early',action='store_true')
parser.add_argument('-B','--baroque',action='store_true')
parser.add_argument('-RO','--romantic',action='store_true')
parser.add_argument('-C','--classical',action='store_true')
parser.add_argument('-N','--nationalistic',action='store_true')
parser.add_argument('-MO','--modern',action='store_true')
parser.add_argument('--misc',action='store_true')

args=vars(parser.parse_args())
print(args)
newGenre=[]
for key,value in args.iteritems():
    if value:
        if key is not 'name' and key is not 'recursive':
            newGenre.append(key)
print(newGenre)
extList=('.flac','.mp3','.m4a','.aiff')
path=args['name']
files=[]
if not args['recursive']:
    print("Scanning...")
    for ext in extList:
        fs=os.path.join(path,'*'+ext)
        print(fs)
        files.append(glob.glob(fs))
        flatten_files=[y for x in files for y in x]

else:
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(extList):
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
        except:
            print("Could not save file!")
