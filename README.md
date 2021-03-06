subtitles-downloader
======================
Subtitles downloader (downloads titles from OpenSubtitles.com)


Dependencies
------------
* python2-magic
* python2-opensubtitles


Author
------
* Otto Sabart - Seberm
* www.seberm.com
* seberm[at]seberm[dot]com


Usage & Options
---------------
```
Usage: subs.py [OPTION]... DIR[S]

subs.py Download subtitles for movies from OpenSubtitles

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit

  Options:
    -r, --recursive     Recursive download throught directories
    -a, --all           Download all found subtitles for specified movie
    -f, --force         Overwrite subtitles if they already exist
    -l LANGUAGE, --language=LANGUAGE
                        Subtitles language (default: eng) [eng, cze, fre, ...,
                        all]
    -d DESTINATIONDIR, --dest-dir=DESTINATIONDIR
                        Directory where subtitles are saved
    --ref-titles=REFTITLES
                        Template subtitles - program will try to find the most
                        similar subtitles in given language
    --log=LOGLEVEL      Set logging level (debug, info, warning, error,
                        critical)

Support: Otto Sabart (www.seberm.com / seberm@seberm.com
```

### Example usage
Downloads the best czech subtitles for all movies in current directory and all subdirectories (recursively):

```
$ cd ~/Movies
$ python2 ~/scripts/subs.py --log=debug --recursive --language=cze ./
```

Download all english subtitles for given movie:
```
$ python2 ~/scripts/subs.py --all ~/Movies/Sherlock.avi
```

Download czech subtitles for given movie which best match english ref-titles:
```
$ python2 ~/scripts/subs.py --language=cze --ref-titles=./ref-eng-titles.srt ./movie.avi
```

Possible language codes you can find [here](https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes).


Todos
-----
```
- Possibility to provide (via params) login and password for OpenSubtitles API
- Use argparse instead of optparse (cause it's deprecated)
```
