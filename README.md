# genretag
A simple script that changes all the genre tags (via taglib) in a directory. The tags are set via flags on the command line. Run ./GenreTag.py -h for help.

Currently only works in python2.7

You need to install taglib and then pytaglib

On the mac using port
```
sudo port install taglib
```
```
pip install pytaglib
```
this failed since it could not find the taglib headers so I had to tell pip where to look
```
pip install --global-option=build_ext --global-option="-I/opt/local/include/" --global-option="-L/opt/local/lib" pytaglib
```