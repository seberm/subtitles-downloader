import pysrt
import math

subs1 = pysrt.open('cze.srt', encoding='iso-8859-1')
subs2 = pysrt.open('eng.srt', encoding='iso-8859-1')

OFFSET = 2

for s1 in subs1:
    s1StartTime = s1.start.seconds + s1.start.minutes * 60 + s1.start.hours * 60 * 60
    s1EndTime = s1.end.seconds + s1.end.minutes * 60 + s1.end.hours * 60 * 60

    print s1.text,

    for s2 in subs2:

        s2StartTime = s2.start.seconds + s2.start.minutes * 60 + s2.start.hours * 60 * 60

        # Zacinaji pobliz startu s1 nejake tiutlky s2?
        if math.fabs(s1StartTime - s2StartTime) > OFFSET:
            # Pokud ano..vypisuje:
            print s2.text

            for foo in subs2:
                if foo.startTime > s2endTime and fooEndTime

    print '--------------------------------------------------------------------------------------------------------------'






