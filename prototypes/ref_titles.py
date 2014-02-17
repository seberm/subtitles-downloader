#/usr/bin/env python2
# -*- coding: utf-8 -*-

import pysrt
import math

subsE = pysrt.open('./eng.srt', encoding='utf-8')
#subsC = pysrt.open('./cze-utf8.srt', encoding='utf-8')
subsC = pysrt.open('./nesedi-utf8.srt', encoding='utf-8')

#cmp1 = []
#offset = 60  # sekund
#time = 0
#
# Zkouska vzorkovani
#for titles in subs:
#    if titles.start.hours * 60 * 60 + titles.start.minutes * 60 + titles.start.seconds > time+offset:
#        cmp1.append(titles)
#        #print("%d:%d:%d\t: %s" % (titles.start.hours, titles.start.minutes, titles.start.seconds, titles.text))
#        time = titles.start.hours * 60 * 60 + titles.start.minutes * 60 + titles.start.seconds + offset


score = 0
offset = 1 # vteriny

for eSub in subsE:
    startSecsEng = eSub.start.hours * 60 * 60 + eSub.start.minutes * 60 + eSub.start.seconds
    endSecsEng = eSub.end.hours * 60 * 60 + eSub.end.minutes * 60 + eSub.end.seconds

    for cSub in subsC:
        startSecsCze = cSub.start.hours * 60 * 60 + cSub.start.minutes * 60 + cSub.start.seconds
        endSecsCze = cSub.end.hours * 60 * 60 + cSub.end.minutes * 60 + cSub.end.seconds
        
        if math.fabs(startSecsEng - startSecsCze) <= offset and math.fabs(endSecsEng - endSecsCze) <= offset:
            print eSub.text.encode('utf-8')
            print cSub.text.encode('utf-8')
            print

            score += 1

print score
