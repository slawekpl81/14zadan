import re, argparse
import sys
from matplotlib import pyplot
import plistlib
import numpy as np
"""
ubuntu:   sudo apt-get install python3-tk 
"""

def readPlist(fileName):
    with open(fileName, 'rb') as fp:
        pl = plistlib.load(fp)
    return pl

def compareId(fileNames):
    allTracks = []
    for fileName in fileNames:
        plist = readPlist(fileName)
        tracks = plist['Tracks']
        for trackId, track in tracks.items():
            try:
                allTracks.append((trackId, track['Name']))
            except:
                pass

    okTracks = 0
    notOkTracks = 0
    for track in allTracks:
        for othertrack in allTracks:
            if track[0] == othertrack[0]:
                if track[1] == othertrack[1]:
                    okTracks += 1
                else:
                    notOkTracks += 1
                    print(f'{track} -- {othertrack}')

    print(f'all tracks are {len(allTracks)} ok tracks are {okTracks} and not ok {notOkTracks}')

def findCommonTracks(fileNames):
    """
    search for shared songs in playlist files and save them to common.txt
    :param fileNames:
    :return:
    """
    trackNameSets = []
    for fileName in fileNames:
        trackNames = set()
        plist = readPlist(fileName)
        tracks = plist['Tracks']
        for trackId, track in tracks.items():
            try:
                trackNames.add(track['Name'])
            except :
                pass
        trackNameSets.append(trackNames)
    commonTracks = set.intersection(*trackNameSets)
    if len(commonTracks)>0:
        f = open('common.txt', 'wb')
        for val in commonTracks:
            s = f'{val}\n'
            f.write(s.encode('UTF-8'))
        f.close()
        print(f'znaleziono {len(commonTracks)} wspolnych utworow')
    else:
        print(f'nie ma zadnych wspolnych utworow')



def ploStats(fileName):
    plist = readPlist(fileName)
    tracks = plist['Tracks']
    ratings = []
    durations = []
    for trackID, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            pass
    if ratings == [] or durations == []:
        print('nie ma zadnych prawidlowych danych')

    x = np.array(durations, np.int32)
    x = x/60000.0
    y = np.array(ratings, np.int32)
    pyplot.subplot(2,1,1)
    pyplot.plot(x,y,'o')
    pyplot.axis([0, 1.05*np.max(x), -1, 110])
    pyplot.xlabel('duration')
    pyplot.ylabel('ratings')

    pyplot.subplot(2,1,2)
    pyplot.hist(x, bins=20)
    pyplot.xlabel('duration')
    pyplot.ylabel('number of tracks')

    pyplot.show()


def findDuplicates(fileName):
    print(f'wyszukiwanie zduplik utw w {fileName}')
    plist = readPlist(fileName)
    tracks = plist['Tracks']
    trackNames = {}
    for trackId, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']
            if name in trackNames:
                if duration//1000 == trackNames[name][0]//1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count+1)
            else:
                trackNames[name] = (duration, 1)
        except:
            pass
    dups = []
    for k,v in trackNames.items():
        if v[1]>1:
            dups.append((v[1], k))
    if len(dups) > 0:
        print(f'znaleziono {len(dups)} duplikatów')
    else:
        print('nie ma duplikatów')
    f = open('dups.txt', 'w')
    for val in dups:
        f.writelines(f'{val[0]}, {val[1]}')
    f.close()



if __name__ == '__main__':
    # fileName = 'maya.xml'
    # test(fileName)
    descStr = """ten program analizuje pliki"""
    
    parser = argparse.ArgumentParser(description=descStr)
    group = parser.add_mutually_exclusive_group()
    
    group.add_argument('--common', nargs='*', dest='plFiles', required=False)
    group.add_argument('--stats', dest='plFile', required=False)
    group.add_argument('--dup', dest='plFileD', required=False)
    group.add_argument('--compId', nargs='*', dest='plFilesC', required=False)

    args = parser.parse_args()

    if args.plFiles:
        findCommonTracks(args.plFiles)
    elif args.plFile:
        ploStats(args.plFile)
    elif args.plFileD:
        findDuplicates(args.plFileD)
    elif args.plFilesC:
        compareId(args.plFilesC)
    else:
        print('not working')