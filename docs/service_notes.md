// https://www.curseforge.com/minecraft/modpacks
// https://minecraft.curseforge.com/projects/245480/files/2512885/download

// DEFAULT_URL = "http://clientupdate-v6.cursecdn.com/feed/addons/432/v10/"
// COMPLETE_URL = DEFAULT_URL + "complete.json.bz2"
// HOURLY_URL = DEFAULT_URL + "hourly.json.bz2"

// https://clientupdate-v6.cursecdn.com/feed/gameversions/432/v10/gameversions.json.bz2

// http://clientupdate-v6.cursecdn.com/feed/addons/432/v10/complete.json.bz2

// "CategorySection": / "Name": "Modpacks"

// Thanks to https://github.com/amcoder/Curse.RestProxy/wiki/Curse-Project-Feed

// GetAllFilesForAddon

// https://github.com/amcoder/Curse.RestProxy/blob/51d40fada96631f3bda652693b141096b20ab597/Curse.RestProxy/Service%20References/AddOnService/AddOnService1.wsdl#L374

// https://findusages.com/search/com.jamesmurty.utils.XMLBuilder2/root$0

// https://addon-service.curse.com/AddOnService.svc?wsdl

// https://addons.forgesvc.net/AddOnService.svc?singleWsdl

// http://www.soapclient.com/soapclient?template=%2Fclientform.html&fn=soapform&SoapTemplate=%2FSoapResult.html&SoapWSDL=https%3A%2F%2Faddons.forgesvc.net%2FAddOnService.svc%3FsingleWsdl&_ArraySize=5

// http://addons.forgesvc.net/AddOnService.svc/binary

// http://addons.forgesvc.net/AddOnService.svc/soap12

// https://logins-v1.curseapp.net/

// https://logins-v1.curseapp.net/help

// https://pastebin.com/hFRgqwGM

// https://pastebin.com/GHDAJcKn


//  https://addons.forgesvc.net/AddOnService.svc/soap12

```
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:add="http://addonservice.curse.com/">
   <soap:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
   	<AuthenticationToken xmlns="urn:Curse.FriendsService:v1" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
   		<ApiKey i:nil="true"></ApiKey>
   		<Token>x</Token>
   		<UserID>y</UserID>
   	</AuthenticationToken>
   	<wsa:Action>http://addonservice.curse.com/IAddOnService/GetAllFilesForAddOn</wsa:Action>
   </soap:Header>
   <soap:Body>
      <add:GetAllFilesForAddOn>
         <add:addOnID>z</add:addOnID>
      </add:GetAllFilesForAddOn>
   </soap:Body>
</soap:Envelope>
```