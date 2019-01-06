#!/usr/bin/env python3

from shutil import copyfile
import re
import glob, os, shutil
import cgi, cgitb
import subprocess
import datetime
import random, string
from time import time
import fileinput
from updateIndex import updateIndex

cgitb.enable()		## allows for debugging errors from the cgi scripts in the browser

form = cgi.FieldStorage()
directory = form.getvalue('location')

if 'local' == form.getvalue('action'):
    ## getting the data from the fields 
    print("Content-type:text/html\r\n\r\n")
    print("<html>")
    print("<head><title>Processing...</title></head>")
    print("<body>")
    print("starting in " + directory +" <br>")
    #os.chdir("/home/dwegmull/web/tmp/")
    size = 640, 640
    print("<form action=\"/cgi-bin/second.py\" id=\"captions\">")
    print("<input type=\"text\" name=\"location\" value=\""+ directory +"\" size=\"100\"><br>")
    print("<input type=\"radio\" name=\"action\" value=\"local\" checked> local<br>")
    print("<input type=\"radio\" name=\"action\" value=\"private\" > publish private<br>")
    print("<input type=\"radio\" name=\"action\" value=\"public\" > publish public<br>")
    print("<input type=\"submit\">")
    print("<table>")
    cover = form.getvalue('cover')
    for file in sorted(os.listdir("/home/dwegmull/cgi-demo/")):
        if (file.endswith('.JPG') or file.endswith('.jpg') or file.endswith('.png') or file.endswith('.PNG')) and not file.startswith('thumbnail'):
            captionName = 'caption-' + file
            if '' == cover:
                cover = file        
            if captionName in form:
                caption = form.getvalue('caption-' + file)
                command = []
                command.append('exiftool')
                command.append('-UserComment=' + caption)
                command.append('-overwrite_original')
                command.append("/home/dwegmull/cgi-demo/" + file)
                result = subprocess.run(command, stdout=subprocess.PIPE)
                comments = []
                comments.append(" ")
            else:
                command = []
                command.append('exiftool')
                command.append('-UserComment')
                command.append("/home/dwegmull/cgi-demo/" + file)
                result = subprocess.run(command, stdout=subprocess.PIPE)
                print(result)
                fields = result.stdout.decode('utf8').split(":")
                comments = fields[1].split("###")
                if len(comments[0]) < 1:
                    caption = ""
                else:
                    caption = comments[0]
            
            print("<tr><td>")
            print("File : " + file)
            print("<a href=\"http://localhost:8000/" + file + "\"><img src=\"http://localhost:8000/thumbnail_"+ file +"\"></a></td>")
            print("<td><textarea name=\"caption-" + file +"\" form=\"captions\" cols=\"80\" rows=\"20\">" + caption + "</textarea></td>")
            if file == cover:
                command = []
                command.append('exiftool')
                command.append('-SequenceNumber=1')
                command.append('-overwrite_original')
                command.append("/home/dwegmull/cgi-demo/" + file)
                result = subprocess.run(command, stdout=subprocess.PIPE)
                command2 = []
                command2.append('exiftool')
                command2.append('-overwrite_original')
                command2.append('-UserComment=' + comments[0] + "###" + form.getvalue('description'))
                command2.append("/home/dwegmull/cgi-demo/" + file)
                print(command2)
                result = subprocess.run(command2, stdout=subprocess.PIPE)
                print("<td><input type=\"radio\" checked name=\"cover\" value=\"" + file + "\">Set as cover picture<td></tr>")
            else:        
                command = []
                command.append('exiftool')
                command.append('-SequenceNumber=0')
                command.append('-overwrite_original')
                command.append("/home/dwegmull/cgi-demo/" + file)
                result = subprocess.run(command, stdout=subprocess.PIPE)
                print("<td><input type=\"radio\" name=\"cover\" value=\"" + file + "\">Set as cover picture<td></tr>")
    print("</table>")
    print("<input type=\"text\" name=\"description\" size=\"100\" value=\"" + form.getvalue('description') + "\"></form>")

    print("</div>")
    print("</body>")
    print("</html>")
else:
    t = int(time())
    t1 = int(t / 100)
    N = 10 + (t - (t1 * 100))
    outDir = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(N))
    os.mkdir("/home/dwegmull/web/" + outDir)
    for basename in os.listdir("/home/dwegmull/cgi-demo"):
        if(basename.endswith('.JPG') or basename.endswith('.jpg') or basename.endswith('.png') or basename.endswith('.PNG')):
            pathname = os.path.join("/home/dwegmull/cgi-demo/", basename)
            if os.path.isfile(pathname):
                shutil.move(pathname, "/home/dwegmull/web/" + outDir)
    file = open("/home/dwegmull/web/" + outDir + "/index.html", "w")
    file.write("<html>")
    file.write("<head><title>album</title></head>")
    file.write("<body>")
    file.write("<p>" + form.getvalue('description') + "</p>")
    file.write("<table>")
    print("Content-type:text/html\r\n\r\n")
    print("<html>")
    print("<head><title>Done</title></head>")
    print("<body>")
    cover = form.getvalue('cover')
    print("cover = " + cover)
    for imgfile in sorted(os.listdir("/home/dwegmull/web/" + outDir)):
        if (imgfile.endswith('.JPG') or imgfile.endswith('.jpg') or imgfile.endswith('.png') or imgfile.endswith('.PNG')) and not imgfile.startswith('thumbnail'):
            captionName = 'caption-' + imgfile
            print(imgfile)
            if '' == cover:
                cover = imgfile
            if captionName in form:
                print("with caption  ")
                caption = form.getvalue('caption-' + imgfile)
                command = []
                command.append('exiftool')
                command.append('-overwrite_original')
                if imgfile == cover:
                    print(" FILE IS COVER")
                    command.append('-UserComment=' + caption + "###" + form.getvalue('description'))
                else:        
                    command.append('-UserComment=' + caption)
                command.append("/home/dwegmull/web/" + outDir + "/" + imgfile)
                result = subprocess.run(command, stdout=subprocess.PIPE)
            else:
                print("no caption  ")
                command = []
                command.append('exiftool')
                command.append('-UserComment')
                command.append("/home/dwegmull/web/" + outDir + "/" + imgfile)
                result = subprocess.run(command, stdout=subprocess.PIPE)
                fields = result.stdout.decode('utf8').split(":")
                if len(fields[1]) < 1:
                    caption = ""
                else:
                    caption = fields[1]
            
            file.write("<tr><td>")
            file.write("<a href=\"" + imgfile + "\"><img src=\"thumbnail_"+ imgfile +"\"></a></td>")
            file.write("<td>" + caption + "</td></tr>")
    file.write("</table>")

    file.write("</div>")
    file.write("</body>")
    file.write("</html>")
    print("<p>Album published. Link will be: http://www.wegmuller.org/" + outDir + "/index.html</p>")
    print(cover)

    updateIndex(form.getvalue('action'), outDir, cover)
    print("<p>Album is public</p>")
    print("</body>")
    print("</html>")

    

