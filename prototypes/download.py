import sys
import os

from pythonopensubtitles.opensubtitles import OpenSubtitles
fd = OpenSubtitles()

class Data(object):
    username = 'down321'
    password = 'downdown'
    name = 'Trance'
    path = ('/home/seberm/Downloads/'
            'Trance.2013 WEBRip XViD juggs')

    video = 'Trance.2013 WEBRip XViD juggs.avi'

    #title = 'Dark.City.1998.Directors.Cut.BRRip.H264.AAC.5.1ch.Gopo.srt'
    #subtitle = 'Dark.City.1998.Directors.Cut.BRRip.H264.AAC.5.1ch.Gopo.srt'


token = fd.login(Data.username, Data.password)
if not token:
    print("Chyba prihlaseni")
    sys.exit(1)

print(token)

from pythonopensubtitles.utils import File
f = File(os.path.join(Data.path, Data.video))
h = f.get_hash()
print("Hash: %s" % h)
print("Size: %f" % f.size)

data = fd.search_subtitles([{'sublanguageid': 'cze', 'moviehash': h, 'moviebytesize': f.size}])

import urllib2
from StringIO import StringIO
import gzip

for item in data:
    print(item['SubDownloadLink'])
    request = urllib2.Request(item['SubDownloadLink'])
    response = urllib2.urlopen(request)

    buf = StringIO(response.read())

    data = gzip.GzipFile(fileobj=buf).read()
    out = open('titles.srt', 'wb')
    out.write(data)
    out.close()

    break

fd.logout()
