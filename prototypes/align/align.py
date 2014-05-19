import pysrt
import math

#subs1 = pysrt.open('cze.srt', encoding='iso-8859-1')
#subs2 = pysrt.open('eng.srt', encoding='iso-8859-1')
subs1 = pysrt.open('eng.srt', encoding='iso-8859-1')
subs2 = pysrt.open('cze.srt', encoding='iso-8859-1')

OFFSET = 1

for s1 in subs1:
    s1StartTime = s1.start.seconds + s1.start.minutes * 60 + s1.start.hours * 60 * 60
    s1EndTime = s1.end.seconds + s1.end.minutes * 60 + s1.end.hours * 60 * 60

    print s1.text.encode('iso-8859-1'),

    end=False
    for s2 in subs2:
        if end:
            break

        s2StartTime = s2.start.seconds + s2.start.minutes * 60 + s2.start.hours * 60 * 60
        s2EndTime = s2.end.seconds + s2.end.minutes * 60 + s2.end.hours * 60 * 60

        # Zacinaji pobliz startu s1 nejake tiutlky s2?
        #print math.fabs(s1StartTime - s2StartTime)
        if math.fabs(s1StartTime - s2StartTime) <= OFFSET:
            # Pokud ano..vypisuje:
            print '\t------\t', s2.text.encode('iso-8859-1')

            for foo in subs2:
                fooStartTime = foo.start.seconds + foo.start.minutes * 60 + foo.start.hours * 60 * 60
                fooEndTime = foo.end.seconds + foo.end.minutes * 60 + foo.end.hours * 60 * 60
                if fooStartTime > s1EndTime:
                    end=True
                    break

                #print fooStartTime,' == ',s2EndTime

                if fooStartTime > s2EndTime:
                    print 20*' ','\t------\t', foo.text.encode('iso-8859-1')
                else:
                    continue

        else:
            continue

    print '--------------------------------------------------------------------------------------------------------------'






