#!/usr/bin/env python3

from bz2 import decompress
import getpass
from io import BytesIO
import json
from os import mkdir
from os.path import exists
import requests
from zeep import Client, xsd
from lxml import etree

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
    modListJSON = json.load(open(modListJSONPath))
  else:
    print('Mod list JSON not exist, fetching it')
    r = requests.get(curseCompleteModListURL)
    decompressedData = decompress(r.content)
    modListJSON = json.loads(decompressedData.decode())
    with open(modListJSONPath, 'wb') as f:
      f.write(decompressedData)
  return modListJSON

curseCompleteModListURL = "http://clientupdate-v6.cursecdn.com/feed/addons/432/v10/complete.json.bz2"
modListJSONPath = 'cache/complete.json'

def main():
  createCacheDirectory('cache')
  modListJSON = updateModListJSON(curseCompleteModListURL, modListJSONPath)
  print(len(modListJSON['data']))
  client = Client('https://addons.forgesvc.net/AddOnService.svc?singleWsdl')

  with client.options(raw_response=True):
    client.service2 = client.bind('AddOnService', 'WsHttpAddOnServiceEndpoint')
    header = xsd.Element(
      '{http://test.python-zeep.org}auth',
        xsd.ComplexType([
          xsd.Element(
            '{http://test.python-zeep.org}username',
            xsd.String()),
        ])
    )
    header_value = header(username='mvantellingen')
    payload = client.create_message(client.service2, 'ListFeeds', _soapheaders=[header_value])

    print(etree.tostring(payload, pretty_print=True).decode())

    # response is now a regular requests.Response object
    # print(response.status_code)
    # print(response.content)

if __name__ == "__main__":
    # execute only if run as a script
    main()
