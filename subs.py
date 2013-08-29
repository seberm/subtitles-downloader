import sys
import os
import logging
from logging import debug, info, error, warning, exception
from optparse import OptionParser, OptionGroup

from StringIO import StringIO
import gzip

try:
    from pythonopensubtitles.opensubtitles import OpenSubtitles
except ImportError:
    exception('Can\'t find pythonopensubtitles module!')


class Data(object):
    username = 'down321'
    password = 'downdown'
    name = 'Trance'
    path = ('/home/seberm/Downloads/'
            'Trance.2013 WEBRip XViD juggs')

    video = 'Trance.2013 WEBRip XViD juggs.avi'




VERSION = '0.1-beta'

class Manager:
    def __init__(self):
        self.fd = OpenSubtitles()


    def __del__(self):
        self.fd.logout()

        '''
        from pythonopensubtitles.utils import File
        f = File(os.path.join(Data.path, Data.video))
        h = f.get_hash()
        print("Hash: %s" % h)
        print("Size: %f" % f.size)

        data = fd.search_subtitles([{'sublanguageid': 'cze', 'moviehash': h, 'moviebytesize': f.size}])

        import urllib2

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
        '''



    def login(self, login, password):
        token = self.fd.login(login, password)
        if not token:
            raise Exception('Can\'t login to OpenSubtitles.org')

        debug('Login token %s' % token)





def main():
    parser = OptionParser(description = '%prog Download subtitles for movies from OpenSubtitles',
                          usage = '%prog [OPTION]... DIR[S]',
                          epilog = 'Support: Otto Sabart (www.seberm.com / seberm@gmail.com',
                          version = '%prog' + VERSION)

    options = OptionGroup(parser, 'Options')
    options.add_option('-r', '--recursive', dest='recursive', action='store_true',
                       help='Recursive download throught directories')


    parser.add_option_group(options)
    (opt, args) = parser.parse_args()


    manager = Manager()
    manager.login(Data.username, Data.password)



if __name__  == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        info('Program interrupted')
        sys.exit(1)


