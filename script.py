from urllib.parse import urlparse
import urllib.parse
from operator import itemgetter
import subprocess
import os
import shutil
from collections import OrderedDict

# MozillaCacheView.exe /stab zzz.txt

pathToMozillaCacheView = "MozillaCacheView.exe"
pathToExtractCache = "./cacheFolder/"
videoDestinationFolder = "./videoFolder/"
pathTofileCacheListFile = "cacheList.txt"

def generateCacheList():
    subprocess.check_output(pathToMozillaCacheView + ' /stab '+ pathTofileCacheListFile, shell=True)


def getCacheList(fileFormat):
    # twitch old video = video/MP2T, filnamnet blir 0.ts 1.ts och 'r k;;rbara en f;r sig
    #Select all video/webm files
    return [line.rstrip('\n').split("\t") for line in open(pathTofileCacheListFile) if fileFormat in line.split("\t")[1] and "woff2" not in line]

def getParameters(files):
    #Create new dict with filenames
    files3 = {}
    for data in files:
        files3[data[0]] = []

    for data in files:
        try:
            # associate filename with server time and url
            files3[data[0]].append([data[10],data[2]])
        except:
            print('exception')
    return files3

def sortFiles(files3):
    # Sort video frames based on server time
    for d in files3:
            files3[d].sort()
    return files3

def sortFilesTW(files3):
    # Sort video frames based on server time
    return OrderedDict(sorted(files3.items(), key = itemgetter(1), reverse = False))

def extractFiles(files3):
    for d in files3:
        for x in files3[d]:
            #print(x[0])
            subprocess.check_output(pathToMozillaCacheView + ' /copycache "'+x[1]+'" "" /CopyFilesFolder '+ pathToExtractCache + ' /UseWebSiteDirStructure 0', shell=True)

def extractFilesTW(files3):
    # extract cachefiles based on url
    for x in files3:
        subprocess.check_output(pathToMozillaCacheView + ' /copycache "'+files3[x][0][1]+'" "" /CopyFilesFolder '+ pathToExtractCache + ' /UseWebSiteDirStructure 0', shell=True)           

def concatenateFiles(files3,live):
    # Get all extracted cachefiles
    cacheFiles = os.listdir(pathToExtractCache)
    if not live:
        # Files are named 1,2,3,... But it will thingk 10 comes after 1
        cacheFiles.sort()

    # Since all twitch-files are named independently just write them to the same file
    with open(videoDestinationFolder+"output.ts", 'wb+') as outFile:
        # Get filename of cachefile in sorted list based on server time
        for outputFile in files3:
            print(outputFile)
        #for outputFile in xd:
            for cacheFile in cacheFiles:
                #print(cacheFile)
                if str(outputFile[0:outputFile.rfind('.')]) in cacheFile:
                    with open(pathToExtractCache+cacheFile, 'rb') as infile:
                        shutil.copyfileobj(infile, outFile)


def concatenateFilesYT(files3):
    cacheFiles = os.listdir(pathToExtractCache)
    # # Files are named name,name=1~,name=2~,... But it will think 10 comes after 1
    cacheFiles.sort(key=lambda f: int(''.join(filter(str.isdigit, f[f.rfind('='):]))))

    
    for outputFile in files3:
        print('put',outputFile)
        with open(videoDestinationFolder+outputFile, 'wb+') as outFile:
            for cacheFile in cacheFiles:
                if str(outputFile[0:outputFile.rfind('.')]) in cacheFile:
                    print('cac',cacheFile)
                    with open(pathToExtractCache+cacheFile, 'rb') as infile:
                        shutil.copyfileobj(infile, outFile)
            

def youtubeLive():
    fileFormat = "video/mp4"
    fileFormat = "video/webm"
    cacheList = getCacheList(fileFormat)
    files3 = getParameters(cacheList)
    sortedList = sortFiles(files3)
    extractFiles(sortedList)
    concatenateFilesYT(sortedList)

def youtube():
    fileFormat = "video/webm"
    cacheList = getCacheList(fileFormat)
    files3 = getParameters(cacheList)
    sortedList = sortFiles(files3)
    extractFiles(sortedList)
    concatenateFilesYT(sortedList)

def twitchLive():
    fileFormat = "application/octet-stream" 
    cacheList = getCacheList(fileFormat)
    files3 = getParameters(cacheList)
    sortedList = sortFilesTW(files3)
    extractFilesTW(sortedList)
    concatenateFiles(sortedList,live=True)
    
def twitch():
    fileFormat = "video/MP2T"
    cacheList = getCacheList(fileFormat)
    files3 = getParameters(cacheList)
    sortedList = sortFilesTW(files3)
    extractFilesTW(sortedList)
    concatenateFiles(sortedList,live=False)

generateCacheList()
youtubeLive()
