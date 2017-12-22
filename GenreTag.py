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
import pprint

def print_info(file):
    print("Tags set on file: {}".format(file))
    try:
        song=taglib.File(file)
    except:
        print("Could not read file for info")
        return
    pprint.pprint(song.tags)               
    
parser=argparse.ArgumentParser(description="Changes the genre tags of the music in a give directoy. If no options are given it prints the existing tags")
parser.add_argument('name',help='directory of music to change. ')
#the optional genre tags
parser.add_argument('-R','--recursive',action='store_true',help="Recursively search directories")

parser.add_argument('-o','--Orchestral',action='store_true')
parser.add_argument('-c','--Chamber',action='store_true')
parser.add_argument('-p','--Opera',action='store_true')
parser.add_argument('-ch','--Choral',action='store_true')
parser.add_argument('-v','--Vocal',action='store_true')
parser.add_argument('-pi','--Piano',action='store_true')
parser.add_argument('-s','--Soundtrack',action='store_true')
parser.add_argument('-j','--Jazz',action='store_true')
parser.add_argument('-r','--PopRock',action='store_true')
parser.add_argument('-x','--Christmas',action='store_true')
parser.add_argument('-m','--Minimalist',action='store_true')
parser.add_argument('-w','--World',action='store_true')

parser.add_argument('-E','--Early',action='store_true')

parser.add_argument('-B','--Baroque',action='store_true')
parser.add_argument('-RO','--Romantic',action='store_true')
parser.add_argument('-C','--Classical',action='store_true')
parser.add_argument('-N','--Nationalistic',action='store_true')
parser.add_argument('-MO','--Modern',action='store_true')
parser.add_argument('--Misc',action='store_true')


parser.add_argument('--named',nargs=1,action='store',help='user specified NAME genre tag')
parser.add_argument('-I','--info',action='store_true', help='print tags of first track and exit')
args=vars(parser.parse_args())
#print(args)
newGenre=[]
for key,value in args.iteritems():
    if value:
        #if key is not 'name' and key is not 'recursive' and key is not 'named':
        if key not in ['name','recursive','named','info']:
            newGenre.append(key)
if args['named'] is not None:
    newGenre.append(args['named'][0])
    
print(newGenre)
#extList=('.flac','.mp3','.m4a','.aiff')
re_extList='.flac$|.mp3$|.m4a$|.aiff$'
path=args['name']
files=[]
if os.path.isdir(path):
    if not args['recursive']:
        print("Scanning...")
        for filename in os.listdir(path):
            if bool(re.search(re_extList,filename,re.I)):
                files.append(os.path.join(path,filename))
                if args['info']:
                    print_info(files[-1])
                
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
                    if args['info']:
                        print_info(files[-1])
else:
#must be a file
    files=[path]
    if args['info']:
        print_info(files[-1])
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
         msg = repr([x.encode(sys.stdout.encoding) for x in song.tags["GENRE"]]).decode('string-escape')
         print("Org. genre tag:"+msg)
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
