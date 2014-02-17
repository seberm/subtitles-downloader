#/usr/bin/env python2
# -*- coding: utf-8 -*-

import pysrt
import math

subsE = pysrt.open('./eng.srt', encoding='utf-8')
subsC = pysrt.open('./cze-utf8.srt', encoding='utf-8')
#subsC = pysrt.open('./nesedi-utf8.srt', encoding='utf-8')
#subsC = pysrt.open('./kratke.srt', encoding='utf-8')

vzorkE = []
time = 0
vzk = 30 # sekund (vzorek)

# Zkouska vzorkovani
for titles in subsE:
    if titles.start.hours * 60 * 60 + titles.start.minutes * 60 + titles.start.seconds > time:
        vzorkE.append(titles)
        time = titles.start.hours * 60 * 60 + titles.start.minutes * 60 + titles.start.seconds + vzk

vzorkC = []
time = 0

# Zkouska vzorkovani
for titles in subsC:
    if titles.start.hours * 60 * 60 + titles.start.minutes * 60 + titles.start.seconds > time:
        vzorkC.append(titles)
        time = titles.start.hours * 60 * 60 + titles.start.minutes * 60 + titles.start.seconds + vzk


score = 0
offset = 1.0 # vteriny

for eSub in vzorkE:
    startSecsEng = eSub.start.hours * 60 * 60 + eSub.start.minutes * 60 + eSub.start.seconds
    endSecsEng = eSub.end.hours * 60 * 60 + eSub.end.minutes * 60 + eSub.end.seconds

    for cSub in vzorkC:
        startSecsCze = cSub.start.hours * 60 * 60 + cSub.start.minutes * 60 + cSub.start.seconds
        endSecsCze = cSub.end.hours * 60 * 60 + cSub.end.minutes * 60 + cSub.end.seconds
        
        if math.fabs(startSecsEng - startSecsCze) <= offset and math.fabs(endSecsEng - endSecsCze) <= offset:
            print eSub.text.encode('utf-8')
            print cSub.text.encode('utf-8')
            print

            score += 1

print score
