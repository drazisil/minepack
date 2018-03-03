#!/usr/bin/env python3

from bz2 import decompress
import getpass
from io import BytesIO
from os import mkdir
from os.path import exists
import requests

def getTwitchLogin():
  username = input("What is your Twitch username? ")
  password = getpass.getpass()

  return username, password

def createCacheDirectory(cacheDirectyPath):
  
  if exists(cacheDirectyPath):
    print('Cache directory already exists')
  else:
    print('Cache directory does not exist, creating it')
    mkdir(cacheDirectyPath)

def updateModListJSON(curseCompleteModListURL, modListJSONPath):
  if exists(modListJSONPath):
    print('Mod list JSON already exists')
  else:
    print('Mod list JSON not exist, fetching it')
    r = requests.get(curseCompleteModListURL)
    with open(modListJSONPath, 'wb') as f:
      f.write(decompress(r.content))
    

curseCompleteModListURL = "http://clientupdate-v6.cursecdn.com/feed/addons/432/v10/complete.json.bz2"
modListJSONPath = 'cache/complete.json'

def main():
  createCacheDirectory('cache')
  updateModListJSON(curseCompleteModListURL, modListJSONPath)

if __name__ == "__main__":
    # execute only if run as a script
    main()
