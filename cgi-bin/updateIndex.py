import subprocess
def updateIndex(rootPath, outDir, cover, caption):
    if outDir.endswith("-public"):
        # public index is only updated isf public. private is always updated.
        f = open(rootPath + 'index.html', "r")
        contents = f.readlines()
        f.close()
        spot = contents.index("<!--start here-->\n")
        contents.insert(spot + 1, "<tr><td align=\"right\"><a href=" + outDir +"/index.html><img src=\"" + outDir + "/thumbnail_" + cover + "\"></td>\n")
        contents.insert(spot + 2, "<td>" + caption + "</td></tr>")
        f = open(rootPath + 'index.html', "w")
        f.writelines(contents)
        f.close()
    f = open(rootPath + 'index-private.html', "r")
    contents = f.readlines()
    f.close()
    spot = contents.index("<!--start here-->\n")
    contents.insert(spot + 1, "<tr><td align=\"right\"><a href=" + outDir +"/index.html><img src=\"" + outDir + "/thumbnail_" + cover + "\"></td>\n")
    contents.insert(spot + 2, "<td>" + caption + "</td></tr>")
    f = open(rootPath + 'index-private.html', "w")
    f.writelines(contents)
    f.close()

def initIndex(rootPath, isPublic):
    if 'public' in isPublic:
        f = open(rootPath + 'index.html', "w")
    else:
        f = open(rootPath + 'index-private.html', "w")
    indexText = '''
<!DOCTYPE html>
<html>
<head>
<title>wegmuller.org</title>
</head>
<body>
<div style="text-align:center;">
    <h1>wegmuller.org</h1></div>
<table>
<tr valign=top><td>
<ul>
<li><a href="http://wegmuller.org/gallery/var/resizes.html">Picture gallery (November 2012 and newer)</a></li>
<li><a href="http://wegmuller.org/v-web/gallery/index.html">Picture Gallery (up to October 2012)</a></li>
<li><a href="http://www.wegmuller.org/riddingcar/riddingcar.html">Ridding car construction</a></li>
<li><a href="http://wegmuller.org/trains/ride_on_scale/index.html">Ride-On Scale Track construction</a></li>
<li><a href="http://wegmuller.org/trains/live_steam/vermod/index.html">The Vermod</a></li>
<li><a href="http://wegmuller.org/trains/live_steam/lego/index.html">Lego live steam!</a></li>
<li><a href="http://wegmuller.org/trains/Gscale/homelayout/index.html">My gauge one layout</a></li>
<li><a href="http://wegmuller.org/trains/Gscale/index.html">Electric G scale trains</a></li>
<li><a href="http://wegmuller.org/trains/HOscale/index.html">Electric HO scale trains</a></li>
<li><a href="http://wegmuller.org/trains/nilesdepot/index.html">Niles Depot</a></li>
<li><a href="http://wegmuller.org/trains/friends/index.html">Models built by my friends</a></li>
<li><a href="http://wegmuller.org/lego/technic/ideas/index.html">Lego Technic ideas</a></li>
<li><a href="http://wegmuller.org/lego/technic/museum/index.html">Old Lego Technic sets</a></li>
<li><a href="http://wegmuller.org/lego/technic/walker/index.html">Mini walking robots</a></li>
<li><a href="http://wegmuller.org/lego/technic/steam_shovel/index.html">Technic fig scale steam shovel</a></li>
<li><a href="http://wegmuller.org/lego/technic/cranes/index.html">Cranes</a></li>
<li><a href="http://wegmuller.org/lego/technic/index.html">Other, older models</a></li>
<li><a href="http://wegmuller.org/lego/space/ships/index.html">Space ships</a></li>
<li><a href="http://wegmuller.org/lego/sculptures/index.html">Sculptures</a></li>
<li><a href="http://wegmuller.org/lego/index.html">Miscelaneous minifig scale models</a></li>
<li><a href="http://wegmuller.org/lego/BayLUG/index.html">BayLUG meetings</a></li>
<li><a href="http://wegmuller.org/logging/index.html">1:20 scale logging equipment</a></li>
<li><a href="http://wegmuller.org/projects/leds/index.html">LED information and simple circuits</a></li>
<li><a href="http://wegmuller.org/trains/full_size/ardenwood/index.html">Ardenwood park in Fremont, CA</a></li>
<li><a href="http://wegmuller.org/trains/full_size/cargill/index.html">Cargill salt in Newark, CA</a></li>
<li><a href="http://wegmuller.org/trains/full_size/roaring_camp/index.html">Roaring Camp in Felton, CA</a></li>
<li><a href="http://wegmuller.org/trains/full_size/wrm/index.html">Western Railway Museum in Rio Vista, CA</a></li>
<li><a href="http://www.wegmuller.org/old_index.html">Old home page</a></li>
</ul>
</td>
<td>
<table>
<!-- The line below is used by the update script to know where to insert gallery updates: do not modify it!!! -->
<!--start here-->
    '''
    f.write(indexText)
    f.close()
