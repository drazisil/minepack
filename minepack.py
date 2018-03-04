#!/usr/bin/env python3

from bz2 import decompress
import getpass
from io import BytesIO
import json
from os import mkdir, getenv
from os.path import exists
import requests
import xml.etree.ElementTree as ET
import ui
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), verbose=True)

def getTwitchLogin():
  if getenv("USERNAME"):
    username = getenv("USERNAME")
  else:
    username = input("What is your Twitch username? ")
  
  if getenv("PASSWORD"):
    password = getenv("PASSWORD")
  else:
    password = getpass.getpass()

  if len(username) == 0 or len(password) == 0:
    print("Either username or password was blank, please try again.")
    getTwitchLogin()
    pass

  return username, password

def getTokenFromTwitch(username, password):
  if getenv("USERID") and getenv("TOKEN"):
      userID = getenv("USERID")
      token = getenv("TOKEN")
  else:
    payload = {'Username': username, 'Password': password}

    r = requests.post("https://logins-v1.curseapp.net/login", data=payload)
    responseJSON = r.json()
    userID = responseJSON['Session']['UserID']
    token = responseJSON['Session']['Token']

  return userID, token

def getAddonID():
  addonID = input("What the modpack id? ")
  return addonID

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

def getAllFilesForAddon(userID, token, addonID):
  getAllFilesForAddonPayload = """<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:add="http://addonservice.curse.com/">
   <soap:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
     <AuthenticationToken xmlns="urn:Curse.FriendsService:v1" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
   	  <ApiKey i:nil="true"></ApiKey>
   	  <Token>{token}</Token>
   	  <UserID>{userID}</UserID>
     </AuthenticationToken>
   	 <wsa:Action>http://addonservice.curse.com/IAddOnService/GetAllFilesForAddOn</wsa:Action>
   </soap:Header>
   <soap:Body>
      <add:GetAllFilesForAddOn>
        <add:addOnID>{addonID}</add:addOnID>
      </add:GetAllFilesForAddOn>
   </soap:Body>
</soap:Envelope>""".format(userID=userID, token=token, addonID=str(addonID))

  headers = {'content-type': 'application/soap+xml'}
  r = requests.post('https://addons.forgesvc.net/AddOnService.svc/soap12', headers=headers, data=getAllFilesForAddonPayload)
  r.headers.get('content-type')
  return(r.text)

curseCompleteModListURL = "http://clientupdate-v6.cursecdn.com/feed/addons/432/v10/complete.json.bz2"
modListJSONPath = 'cache/complete.json'

def main():
  createCacheDirectory('cache')
  modListJSON = updateModListJSON(curseCompleteModListURL, modListJSONPath)
  print(len(modListJSON['data']))

  username, password = getTwitchLogin()
  userID, token = getTokenFromTwitch(username, password)

  addonID = getAddonID()

  fileListingXML = getAllFilesForAddon(userID, token, addonID)

  root = ET.fromstring(fileListingXML)

  modPackVersions = {}

  for child in root[1][0][0]:
    downloadURL = child[2].text
    modPackVersions[downloadURL] = downloadURL

  selected_fruit = ui.ask_choice("Choose a fruit", sorted(modPackVersions.keys()))

  print(modPackVersions[selected_fruit])

if __name__ == "__main__":
    # execute only if run as a script
    main()
