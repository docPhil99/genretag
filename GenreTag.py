#! /usr/bin/python
"""A simple script that changes all the genre tags (via taglib) in a directory. The tags are set via flags on the command line. Run ./GenreTag -h for help. """


import os
import sys
import taglib
import argparse
import re
import pprint

def get_file_list(args):
    re_extList = '.flac$|.mp3$|.m4a$|.aiff$'
    path = args['path']
    files = []
    if os.path.isdir(path):
        if not args['recursive']:
            print("Scanning...")
            for filename in os.listdir(path):
                if bool(re.search(re_extList, filename, re.I)):
                    files.append(os.path.join(path, filename))
                    if args['info']:
                        print_info(files[-1])
                        sys.exit(0)


        else:
            for root, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    if bool(re.search(re_extList, filename, re.I)):
                        files.append(os.path.join(root, filename))
                        if args['info']:
                            print_info(files[-1])
                            sys.exit(0)
    else:
        # must be a file
        files = [path]
        if args['info']:
            print_info(files[-1])
            sys.exit(0)
    return files

def print_info(file):
    print("Tags set on file: {}".format(file))
    try:
        with taglib.File(file) as _song:
            pprint.pprint(_song.tags)

    except:
        print("Could not read file for info")
        return

parser=argparse.ArgumentParser(description="Changes the genre tags of the music in a give directory. If no options are given it prints the existing tags")
parser.add_argument('path',help='directory of music to change. ')
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

parser.add_argument('-l','--Lieder',action='store_true')
parser.add_argument('-B','--Baroque',action='store_true')
parser.add_argument('-RO','--Romantic',action='store_true')
parser.add_argument('-C','--Classical',action='store_true')
parser.add_argument('-N','--Nationalistic',action='store_true')
parser.add_argument('-MO','--Modern',action='store_true')
parser.add_argument('--Misc',action='store_true')


parser.add_argument('--named',nargs=1,action='store',help='user specified NAME genre tag')
parser.add_argument('-I','--info',action='store_true', help='print tags of first track and exit')
args=vars(parser.parse_args())

# get the list of new genres from argparse. Ignore general options.
newGenre=[]
for key,value in args.items():
    if value:
        #if key is not 'name' and key is not 'recursive' and key is not 'named':
        if key not in ['path','recursive','named','info']:
            newGenre.append(key)
if args['named'] is not None:
    newGenre.append(args['named'][0])
    
print(f'Setting genre to {newGenre}')

flatten_files = get_file_list(args)

if len(flatten_files)==0:
    sys.exit("No supported media file found")
else:
    print(f'Found {len(flatten_files)} files')

if len(newGenre)==0:
    print("No new genre tags set. Exiting.")
    sys.exit(0)

for file in flatten_files:
    print(f'File: {file}')
    try:
        with taglib.File(file, save_on_exit=True) as song:
            if "GENRE" in song.tags.keys():
                msg = song.tags["GENRE"]
                print("Org. genre tag:")
                print(', '.join(msg))
            else:
                print("No current tag set")
            song.tags["GENRE"] = newGenre
            print("Set to new genre ")
            print(', '.join(newGenre))
    except OSError as e:
        print(f"Could not read/save file {file}\n{e.message}")
        continue
    
