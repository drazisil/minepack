#!/usr/bin/env python3

from bz2 import decompress
import getpass
from io import BytesIO
import json
from os import mkdir
from os.path import exists
import requests

def getTwitchLogin():
  username = input("What is your Twitch username? ")
  password = getpass.getpass()

  return username, password

def getTokenFromTwitch(username, password):
  payload = {'Username': username, 'Password': password}

  r = requests.post("https://logins-v1.curseapp.net/login", data=payload)
  responseJSON = r.json()
  userID = responseJSON['Session']['UserID']
  token = responseJSON['Session']['Token']
  return userID, token

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

def getAllFilesForAddon(userID, Token, addonID):
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



  print(getAllFilesForAddonPayload)
  headers = {'content-type': 'application/soap+xml'}
  r = requests.post('https://addons.forgesvc.net/AddOnService.svc/soap12', headers=headers, data=getAllFilesForAddonPayload)

  print(r.text)
  pass

curseCompleteModListURL = "http://clientupdate-v6.cursecdn.com/feed/addons/432/v10/complete.json.bz2"
modListJSONPath = 'cache/complete.json'

def main():
  createCacheDirectory('cache')
  modListJSON = updateModListJSON(curseCompleteModListURL, modListJSONPath)
  print(len(modListJSON['data']))

  username, password = getTwitchLogin()
  userID, token = getTokenFromTwitch(username, password)


if __name__ == "__main__":
    # execute only if run as a script
    main()
