#!/usr/bin/env python3

from PIL import Image
from shutil import copyfile
import re
import glob, os, shutil
import cgi, cgitb
import subprocess
import datetime
import random, string
from time import time
import fileinput
from PIL.ExifTags import TAGS
cgitb.enable()		## allows for debugging errors from the cgi scripts in the browser

form = cgi.FieldStorage()

## getting the data from the fields 
directory = form.getvalue('location')
print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head><title>Processing...</title></head>")
print("<body>")
print("starting in " + directory +" <br>")
#os.chdir("/home/dwegmull/web/tmp/")
size = 500, 500
print("<form action=\"/cgi-bin/twocolumn2.py\" id=\"captions\">")
print("<input type=\"text\" name=\"location\" value=\""+ directory +"\"><br>")
print("<input type=\"radio\" name=\"action\" value=\"local\" checked> local<br>")
print("<input type=\"radio\" name=\"action\" value=\"private\" > publish private<br>")
print("<input type=\"radio\" name=\"action\" value=\"public\" > publish public<br>")
print("<input type=\"text\" name=\"description\" size=\"100\" value=\"Posted on "+ str(datetime.date.today()) +"\">")
print("<input type=\"submit\">")
print("<table>")
counter = 0;
for imgfile in sorted(os.listdir(directory)):
    if imgfile.endswith('.JPG') or imgfile.endswith('.jpg') or imgfile.endswith('.png') or imgfile.endswith('.PNG'):
        if counter & 0x01:
            print("<td>")
        else:
            print("<tr><td>")
        print("File : " + imgfile)
        copyfile(directory + "/" + imgfile, "/home/dwegmull/cgi-demo/%s" % imgfile)
        command = []
        command.append('exiftool')
        command.append('-UserComment=' + imgfile)
        command.append('-overwrite_original')
        command.append('-Artist=David Wegmuller')
        command.append('-Copyright=Copyright David@Wegmuller.org, all rights reserved')
        command.append("/home/dwegmull/cgi-demo/" + "/" + imgfile)
        result = subprocess.run(command, stdout=subprocess.PIPE)
        caption = imgfile
        im = Image.open("/home/dwegmull/cgi-demo/" + "/" + imgfile)
        for orientation in TAGS.keys() : 
            if TAGS[orientation]=='Orientation' : break 
        exif=dict(im._getexif().items())

        if   exif[orientation] == 3 : 
            im=im.rotate(180, expand=True)
        elif exif[orientation] == 6 : 
            im=im.rotate(270, expand=True)
        elif exif[orientation] == 8 : 
            im=im.rotate(90, expand=True)
        im.thumbnail(size)
        im.save("/home/dwegmull/cgi-demo/thumbnail_%s" % (imgfile))
        print("<a href=\"http://localhost:8000/" + imgfile + "\"><img src=\"http://localhost:8000/thumbnail_"+ imgfile +"\"></a></td>")
        print("<td><input type=\"radio\" name=\"cover\" value=\"" + imgfile + "\">Set as cover picture</td>")
        if counter & 0x01:
            print("</tr>")
        counter += 1
        
if counter & 0x01:
    print("</tr>")
print("</table></form>")

print("</div>")
print("</body>")
print("</html>")
      
            
