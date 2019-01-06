import subprocess
import os
import itertools
from PIL import Image
from PIL.ExifTags import TAGS
import argparse
from updateIndex import initIndex
from updateIndex import updateIndex
#Thumbnail max width and height
size = 640, 640
# path to the local web mirror
rootPath = '/home/dwegmull/web/'

# command line arguments.
parser = argparse.ArgumentParser()
parser.add_argument("--noThumbs", help="Don't generate the thumbnails", action="store_true")
args = parser.parse_args()

# for each subdir (album) save a link to its cover picture and its description
coverPictures = []
descriptions = []
creationTimes = []
for root, subdirs, files in os.walk(rootPath):
    for subdir in subdirs:
        # new directory: remove its index file if present and create a new one.
        indexPath = root + subdir + "/index.html"
        if os.path.exists(indexPath):
            os.remove(indexPath)
        indexFile = open(indexPath, "w")
        indexFile.write("<html>")
        indexFile.write("<head><title>album</title></head>")
        indexFile.write("<body>")
        
        command = []
        command.append('exiftool')
        command.append('-UserComment')
        command.append('-SequenceNumber')
        command.append('-overwrite_original')
        command.append('-ext')
        command.append('JPG')
        command.append('-ext')
        command.append('jpg')
        command.append('-fileOrder')
        command.append('DateTimeOriginal')
        command.append(root + subdir)
        result = subprocess.run(command, stdout=subprocess.PIPE)
        lines = result.stdout.decode('utf8').split('\n')
        # Each file takes up to three lines of output and there are many lines that are not valid files. 
        # We use only even entries, so reserving 2 * size / 3 is safe.
        fileNames = [' '] * int(2 *len(lines) / 3)
        captions = [' '] * int(2 * len(lines) / 3)
        tempName = ''
        tempNumber = '0'
        tempCaption = ''
        indexCounter = 2
        albumDescription = ''
        for line in lines:
            if 'thumbnail_' not in line:
                if line.startswith("========") :
                    # if this is not the first file, place the previous one and its data in to the tables.
                    if tempName is not '' :
                        index = int(tempNumber)
                        
                        if (0 == index) or ((1 == index) and (fileNames[1] is not ' ')):
                            index = indexCounter
                            indexCounter = indexCounter + 2
                        fileNames[index] = tempName
                        captions[index] = tempCaption
                        if 1 == index:
                            # cover picture: save its details.
                            coverPictures.append(subdir + "/" + tempName)
                            creationTimes.append(os.path.getmtime(root + "/" + subdir + "/" + tempName))
                        
                    tempNumber = '0'
                    tempCaption = ''
                    # new file: remove its old thumbnail, if present and create a fresh one.
                    fields = line.split(" ")
                    head, tail = os.path.split(fields[1])
                    tempName = tail
                    if not args.noThumbs :
                        thumbPath = head + "/thumbnail_" + tail
                        if os.path.exists(thumbPath):
                            os.remove(thumbPath)
                        print(fields[1])
                        im = Image.open(fields[1])
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
                        im.save(thumbPath)
                else :
                    fields = line.split(':')
                    if 'User Comment' in fields[0]:
                        commentFields = fields[1].split("###")
                        tempCaption = commentFields[0]
                        if len(commentFields) > 1:
                            albumDescription = albumDescription + commentFields[1]
                    else:
                        if 'Sequence Number' in fields[0]:
                            tempNumber = fields[1]
                        else :
                            if ('directories scanned' not in line) and ('image files read' not in line) :
                                tempCaption = tempCaption + line
        #process the last file in the directory
        if tempName is not '' :
            index = int(tempNumber)
            if (0 == index) or ((1 == index) and (fileNames[1] is not ' ')):
                index = indexCounter
                indexCounter = indexCounter + 2
            fileNames[index] = tempName
            captions[index] = tempCaption
        descriptions.append(albumDescription)
        if len(coverPictures) < len(descriptions) :
            # This album has no cover photo: just pick the last one as cover.
            coverPictures.append(subdir + "/" + tempName)
        if len(creationTimes) < len(descriptions) :
            # This album has no creation time: use the one of the last photo.
            creationTimes.append(os.path.getmtime(root + "/" + subdir + "/" + tempName))
        # Write the rest of index.html
        indexFile.write("<p>" + albumDescription + "</p>")
        indexFile.write("<table>")

        for fileName, caption in itertools.zip_longest(fileNames, captions, fillvalue=' '):
            if fileName is not ' ':
                indexFile.write("<tr><td>")
                indexFile.write("<a href=\"" + fileName + "\"><img src=\"thumbnail_"+ fileName +"\"></a></td>")
                indexFile.write("<td>" + caption + "</td></tr>")
        indexFile.write("</table>")

        indexFile.write("</div>")
        indexFile.write("</body>")
        indexFile.write("</html>")
                
        indexFile.close()
#remove / init the index files
if os.path.exists(rootPath + 'index.html'):
    os.remove(rootPath + 'index.html')
if os.path.exists(rootPath + 'index-private.html'):
    os.remove(rootPath + 'index-private.html')
initIndex(rootPath, 'public')
initIndex(rootPath, 'private')
while len(coverPictures) > 0:
    newest = 0
    newestIndex = 0
    i = 0
    for coverPicture, description, creationTime in itertools.zip_longest(coverPictures, descriptions, creationTimes):
        print(coverPicture, description, creationTime)
        if creationTime > newest :
            newest = creationTime
            newestIndex = i
        i = i + 1
    head, tail = os.path.split(coverPictures[newestIndex])
    updateIndex(rootPath, head, tail, descriptions[newestIndex])
      
    del coverPictures[newestIndex]
    del descriptions[newestIndex]
    del creationTimes[newestIndex]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
