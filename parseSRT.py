import sys
import re
import copy
import json

files = sys.argv[1:]

def parseFilename(string):
    form1 = r"[sS](\d\d?)[eE](\d\d?)"
    form2 = r"(\d\d?)x(\d\d?)"
    form3 = r"\[(\d\d?)\.(\d\d?)"

    for regexp in [form1,form2,form3]:
        matches = re.findall(regexp,string)
        if len(matches) > 0:
            return matches[0]

    return ("",re.sub(".*Episode (\d\d).*",r"\1",string))

def readSRTfile(filename,presentParams):
    print filename
    blocks = "".join(open(filename).readlines())
    blocks = re.sub(r"\r","",blocks)
    blocks = blocks.split("\n\n")
    blocks = [block.split("\n") for block in blocks]

    values = []
    for block in blocks:
        metadata = copy.deepcopy(presentParams)
        num = block[0]
        try:
            times = re.findall("^\d\d:(\d\d):(\d\d)",block[1])[0]
        except IndexError:
            continue
        #Let's one-index the minutes.
        metadata["minute"] = int(times[0]) + 1
        metadata["second"] = int(times[1]) + int(times[0])*60

        metadata["filename"] = "%(season)i-%(ep)i-%(minute)i-%(second)i" % metadata
        metadata["text"] = " ".join(block[2:])
        metadata["searchstring"] = "Season %(season)i, Episode %(ep)i: <i>%(text)s</i>" %metadata
        values.append(metadata)
    return values


if __name__=="__main__":
    fullList = []
    for filename in files:
        (season,ep) = parseFilename(filename)
        try:
            season = int(season)
        except:
            season = 0
        ep = int(ep)
        fullList.append((season,ep,filename))
    #Sort by season and episode
    fullList.sort()
    episode_number = 0
    jsoncatalog = open("jsoncatalog.txt","w")
    inputtxt = open("input.txt","w")

    for episode in fullList:
        episode_number += 1
        (season,ep,filename) = episode
        values = readSRTfile(filename,{"season":season,"ep":ep,"episodeNumber":episode_number})
        for value in values:
            try:
                inputtxt.write("%(filename)s\t%(text)s\n"%value)
                jsoncatalog.write(json.dumps(value).encode("utf-8") + "\n")
            except UnicodeDecodeError:
                pass
    jsoncatalog.close()
    inputtxt.close()
                    
