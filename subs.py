import sys
import os
import logging
import urllib2
import magic

from logging import debug, info, error, warning, exception
from optparse import OptionParser, OptionGroup

from StringIO import StringIO
import gzip

try:
    from pythonopensubtitles.opensubtitles import OpenSubtitles
    from pythonopensubtitles.utils import File
except ImportError:
    exception('Can\'t find pythonopensubtitles module!')
    sys.exit(99)


class Data(object):
    username = 'down321'
    password = 'downdown'


VERSION = '0.1-beta'
DEFAULT_LOGGING_LEVEL = 'info'
DEFAULT_LOGGING_FORMAT = '%(levelname)s: %(message)s'

DEFAULT_SUBTITLES_LANGUAGE = 'eng'
VIDEO_MIME_TYPES = [
    'application/annodex',
    'application/mp4',
    'application/ogg',
    'application/vnd.rn-realmedia',
    'application/x-matroska',
    'video/3gpp',
    'video/3gpp2',
    'video/annodex',
    'video/divx',
    'video/flv',
    'video/h264',
    'video/mp4',
    'video/mp4v-es',
    'video/mpeg',
    'video/mpeg-2',
    'video/mpeg4',
    'video/ogg',
    'video/ogm',
    'video/quicktime',
    'video/ty',
    'video/vdo',
    'video/vivo',
    'video/vnd.rn-realvideo',
    'video/vnd.vivo',
    'video/webm',
    'video/x-bin',
    'video/x-cdg',
    'video/x-divx',
    'video/x-dv',
    'video/x-flv',
    'video/x-la-asf',
    'video/x-m4v',
    'video/x-matroska',
    'video/x-motion-jpeg',
    'video/x-ms-asf',
    'video/x-ms-dvr',
    'video/x-ms-wm',
    'video/x-ms-wmv',
    'video/x-msvideo',
    'video/x-sgi-movie',
    'video/x-tivo',
    'video/avi',
    'video/x-ms-asx',
    'video/x-ms-wvx',
    'video/x-ms-wmx'
]

def videoFiletype(file):
    mimeType = magic.from_file(file, mime=True)

    if mimeType in VIDEO_MIME_TYPES:
        debug("Detected mime-type: %s" % mimeType)
        return True
    else:
        return False

def confirm(msg):
    yes = ['yes', 'y']
    no = ['no', 'n', '']

    while True:
        print msg + "[y/N]:",
        ch = raw_input().lower()
        if ch in yes:
            return True
        elif ch in no:
            return False
        else:
            info("Unrecognized choice")


class Manager:
    __fd = None
    __subtitleCounter = 0


    def __init__(self, args, language=DEFAULT_SUBTITLES_LANGUAGE):
        debug('Logging to OpenSubtitles.org API server')
        self.__fd = OpenSubtitles()
        self.__recursiveDownload = False
        self.__downloadAll = False
        self.__destination = None
        self.__language = language
        self.__force = False
        self.__refTitles = None
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


    def setForce(self, opt=True):
        self.__force = opt


    def setRefTitles(self, t):
        self.__refTitles = t


    def setDestination(self, dest):
        self.__destination = dest


    def downloadAllSubtitles(self, opt=True):
        self.__downloadAll = opt


    def download(self):
        for arg in self.__args:
            self.__downloadSubtitles(arg)


    def __get(self, title, f):
        debug('[%s] Download link: %s' % (os.path.basename(f), title['SubDownloadLink']))

        request = urllib2.Request(title['SubDownloadLink'])
        response = urllib2.urlopen(request)
        buf = StringIO(response.read())
        data = gzip.GzipFile(fileobj=buf).read()
        dir = os.path.dirname(f)
        if self.__destination:
            dir = self.__destination

        postfix = ''
        if self.__downloadAll:
            postfix = "_%d"  % self.__subtitleCounter
            self.__subtitleCounter += 1

        subFilename = os.path.join(dir, os.path.splitext(os.path.basename(f))[0] + postfix + "." + title['SubFormat'])
        if os.path.isfile(subFilename) and not self.__force:
            if not confirm("Subtitle file already exists. Do you really want to overwrite it?"):
                debug("We're not overwriting ...")
                return

        with open(subFilename, 'wb') as out:
            out.write(data)


    def __getSubFile(self, f):
        basename = os.path.basename(f)
        if not videoFiletype(f):
            debug('File is not a video: %s' % basename)
            return

        debug('Searching for titles: %s' % basename)

        movie = File(f)
        debug("[%s] Hash: %s" % (basename, movie.get_hash()))
        debug("[%s] Size: %d Bytes" % (basename, movie.size))
        subtitleData = self.__fd.search_subtitles([{'sublanguageid': self.__language, 'moviehash': movie.get_hash(), 'moviebytesize': movie.size}])

        if not subtitleData:
            error('[%s] No subtitles found (maybe incorrect movie file?)' % basename)
            return

        debug("[%s] Found %d subtitles" % (basename, len(subtitleData)))

        if self.__downloadAll:
            for subs in subtitleData:
                if self.__downloadAll:
                    self.__get(subs, f)
        else:
            # We try to find the best subtitles for our movie
            bestSubtitles = self.__findBestTitles(subtitleData)
            if bestSubtitles:
                debug("[%s] Downloading the BEST subtitles" % basename)
                self.__get(bestSubtitles, f)


    def __findBestTitles(self, subtitles):
        '''Get subtitles with the big number of downloads'''
        bestSubtitles = None
        for subs in subtitles:
            # TODO There will be algorithm for finding the best subtitles
            if not bestSubtitles or int(subs['SubDownloadsCnt']) > int(bestSubtitles['SubDownloadsCnt']):
                bestSubtitles = subs

        return bestSubtitles


    def __downloadSubtitles(self, path):
        '''Download subtitles for every movie in specified directory'''
        rPath = os.path.realpath(path)
        if os.path.isdir(rPath):
            for f in os.listdir(rPath):
                nextPath = os.path.join(rPath, f)
                if os.path.isdir(os.path.join(rPath, f)) and self.__recursiveDownload:
                    self.__downloadSubtitles(nextPath)
                else:
                    self.__getSubFile(nextPath)
        else:
            self.__getSubFile(rPath)



def main():
    parser = OptionParser(description = '%prog Download subtitles for movies from OpenSubtitles',
                          usage = '%prog [OPTION]... DIR[S]',
                          epilog = 'Support: Otto Sabart (www.seberm.com / seberm@seberm.com',
                          version = '%prog' + VERSION)

    options = OptionGroup(parser, 'Options')
    options.add_option('-r', '--recursive', dest='recursiveDownload', action='store_true', default=False,
                       help='Recursive download throught directories')
    options.add_option('-a', '--all', dest='allSubtitles', action='store_true', default=False,
                       help='Download all found subtitles for specified movie')
    options.add_option('-f', '--force', dest='force', action='store_true', default=False,
                       help='Overwrite subtitles if they already exist')
    options.add_option('-l', '--language', dest='language', action='store', default=DEFAULT_SUBTITLES_LANGUAGE,
                       help='Subtitles language (default: eng) [eng, cze, fre, ..., all]')
    options.add_option('-d', '--dest-dir', dest='destinationDir', action='store',
                       help='Directory where subtitles are saved')
    options.add_option('--ref-titles', dest='refTitles', action='store',
                       help='Template subtitles - program will try to find the most similar subtitles in given language')
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

    if not args:
        error('It\'s necessary to provide at least one argument')
        sys.exit(1)

    manager = Manager(args, language=opt.language)
    manager.login(Data.username, Data.password)
    manager.setRecursiveDownload(opt.recursiveDownload)
    manager.setForce(opt.force)

    if opt.refTitles:
        if opt.recursiveDownload:
            error("You cannot use --recursive and --ref-titles arguments togetner. Exiting ...")
            return

        manager.setRefTitles(opt.refTitles)

    if opt.allSubtitles:
        manager.downloadAllSubtitles()

    if opt.destinationDir:
        manager.setDestination(opt.destinationDir)

    manager.download()



if __name__  == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        info('Program interrupted')
        sys.exit(1)


