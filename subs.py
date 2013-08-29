import sys
import os
import logging
import urllib2

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
DEFAULT_LOGGING_LEVEL = 'info'
DEFAULT_LOGGING_FORMAT = '%(levelname)s: %(message)s'

DEFAULT_SUBTITLES_LANGUAGE = 'eng'
VIDEO_TYPES = ['mp4', 'avi', 'wmv']


def videoFiletype(file):
    postfix = file.split(".")[-1]
    if postfix in VIDEO_TYPES:
        return True
    else:
        return False



class Manager:
    __fd = None


    def __init__(self, args, language=DEFAULT_SUBTITLES_LANGUAGE):
        debug('Logging to OpenSubtitles.org API server')
        self.__fd = OpenSubtitles()
        self.__recursiveDownload = False
        self.__language = language
        debug('Subtitle language is set to [%s]' % self.__language)

        self.__args = args


    def __del__(self):
        debug('Logouting from OpenSubtitles.org API server')
        self.__fd.logout()


    def login(self, login, password):
        token = self.__fd.login(login, password)
        if not token:
            raise Exception('Can\'t login to OpenSubtitles.org')

        debug('Login token %s' % token)


    def setRecursiveDownload(self, opt=True):
        self.__recursiveDownload = opt


    def download(self):
        for arg in self.__args:
            self.__downloadSubtitles(arg)


    def __downloadSubtitles(self, path):
        '''Download subtitles for every movie in specified directory'''

        if os.path.isdir(path):
            for f in os.listdir(path):
                if self.__recursiveDownload:
                    self.__downloadSubtitles(os.path.join(path, f))

                if not videoFiletype(f):
                    continue
                else:
                    debug('Finding titles for: %s' % f)

                    from pythonopensubtitles.utils import File
                    movie = File(os.path.join(path, f))
                    debug("[%s] Hash: %s" % (f, movie.get_hash()))
                    debug("[%s] Size: %d Bytes" % (f, movie.size))
                    subtitleData = self.__fd.search_subtitles([{'sublanguageid': self.__language, 'moviehash': movie.get_hash(), 'moviebytesize': movie.size}])
                    debug("[%s] Found %d subtitles" % (f, len(subtitleData)))

                    # Get subtitles with the big number of downloads
                    bestSubtitles = None
                    for subs in subtitleData:
                        if not bestSubtitles or int(subs['SubDownloadsCnt']) > int(bestSubtitles['SubDownloadsCnt']):
                            bestSubtitles = subs

                    if not bestSubtitles:
                        error('[%s] No subtitles found' % f)
                        continue

                    debug('[%s] Download link: %s' % (f, bestSubtitles['SubDownloadLink']))

                    request = urllib2.Request(bestSubtitles['SubDownloadLink'])
                    response = urllib2.urlopen(request)
                    buf = StringIO(response.read())
                    data = gzip.GzipFile(fileobj=buf).read()
                    with open(os.path.join(path, os.path.splitext(f)[0] + '.srt'), 'wb') as out:
                        out.write(data)




def main():
    parser = OptionParser(description = '%prog Download subtitles for movies from OpenSubtitles',
                          usage = '%prog [OPTION]... DIR[S]',
                          epilog = 'Support: Otto Sabart (www.seberm.com / seberm@gmail.com',
                          version = '%prog' + VERSION)

    options = OptionGroup(parser, 'Options')
    options.add_option('-r', '--recursive', dest='recursiveDownload', action='store_true', default=False,
                       help='Recursive download throught directories')
    options.add_option('-l', '--language', dest='language', action='store', default=DEFAULT_SUBTITLES_LANGUAGE,
                       help='Subtitles language (default: eng)')
    options.add_option('-d', '--dest-dir', dest='destinationDir', action='store',
                       help='Directory where subtitles are saved')
    options.add_option('--log', dest='logLevel', action='store', default=DEFAULT_LOGGING_LEVEL,
                        help='Set logging level (debug, info, warning, error, critical)')


    parser.add_option_group(options)
    (opt, args) = parser.parse_args()


    # Logging stuff
    try:
        logging.basicConfig(format=DEFAULT_LOGGING_FORMAT, level=opt.logLevel.upper())
        debug('Setting logging mode to: %s' % opt.logLevel.upper())
    except ValueError:
        logging.basicConfig(format=DEFAULT_LOGGING_FORMAT, level=DEFAULT_LOGGING_LEVEL)
        warning('It is not possible to set logging level to %s' % opt.logLevel.upper())
        warning('Using default setting logging level: %s' % DEFAULT_LOGGING_LEVEL)



    if opt.destinationDir:
        debug('Changing default program directory to %s' % opt.destinationDir)
        os.chdir(opt.destinationDir)

    if not args:
        error('It\'s necessary to provide at least one argument')
        sys.exit(1)

    manager = Manager(args, language=opt.language)
    manager.login(Data.username, Data.password)
    manager.setRecursiveDownload(opt.recursiveDownload)

    manager.download()



if __name__  == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        info('Program interrupted')
        sys.exit(1)


