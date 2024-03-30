import warnings
warnings.filterwarnings("ignore")

__author__ = 'mr moorgh'
__version__ = 1.6

from sys import version_info
if version_info[0] == 2: # Python 2.x
    from mrweb import *
elif version_info[0] == 3: # Python 3.x
    from mrweb.mrweb import *

import os
##############################################
def installlib():
    try:
        os.system("pip install requests")
    except:
        try:
            os.system("pip3 install requests")
        except:
            try:
                os.system("python3 -m pip install requests")
            except:
                os.system("python -m pip install requests")
    return True


##############################################
try:
    import requests
except:
    installlib()
    import requests
import json


version="1.6"
apikey = ""



class AIError(Exception):
    pass

class TranslateError(Exception):
    pass

class NoInternet(Exception):
    pass

class JsonError(Exception):
    pass

class NoCoin(Exception):
    pass

class EndSupport(Exception):
    pass

def getlatest():
    version = "1.6"
    api=requests.get("https://mrapiweb.ir/mrapi/update.php?version={version}").text
    js=json.loads(api)
    if js["update"] == False:
        try:
            os.system("pip install mrweb --upgrade")
        except:
            try:
                os.system("pip3 install mrweb --upgrade")
            except:
                try:
                    os.system("python3 -m pip install mrweb --upgrade")
                except:
                    os.system("python -m pip install mrweb --upgrade")
    else:
        return True
def setapikey(key):
    global apikey
    apikey = key
    
class ai():
    def bard(query):
        raise EndSupport("Bard Moved To Gemini!") from None
    def gpt(query):
        global apikey
        query=query.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/chatbot.php?key={apikey}&question={query}").text
        try:
            result=json.loads(api)
        except json.decoder.JSONDecodeError:
            raise AIError(api) from None
        
        try:
            return result["javab"]
        except Exception as er:
            raise AIError("Failed To Get Answer Make Sure That You Are Connected To Internet & vpn is off") from None
        
    def evilgpt(query):
        
        api=requests.get(f"https://mrapiweb.ir/api/evilgpt.php?key=testkey&emoji=🗿&soal={query}").text
        result=json.loads(api)
        try:
            return result["javab"]
        except KeyError:
            raise NoCoin("Please Charge Your Key From @mrapiweb_bot") from None
            
        except Exception as er:
            raise AIError("Failed To Get Answer Make Sure That You Are Connected To Internet & vpn is off") from None
    def gemini(query):
        query=query.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/geminiai.php?question={query}").text
        try:
            return api
        except:
            raise AIError("No Answer Found From Gemini. Please Try Again!")
    def codeai(query):
        query = query.replace(" ","+")
        api=requests.get(f"https://mrapiweb.ir/api/aiblack.php?soal={query}").text
        try:
            return api
        except:
            raise AIError("No Answer Found From CodeAI. Please Try Again!") from None

        

class api():
    def translate(to,text):
        api=requests.get(f"https://mrapiweb.ir/api/translate.php?to={to}&text={text}").text
        result=json.loads(api)
        try:
            return result["translate"]
        except KeyError:
            raise TranslateError("Translate Error For Lang {to}") from None
        
    def ocr(to,url):
        api=requests.get(f"https://mrapiweb.ir/api/ocr.php?url={url}&lang={to}").text
        result=json.loads(api)
        try:
            return result["result"]
        except KeyError:
            raise AIError("Error In OCR Lang {to}") from None
    def isbadword(text):
        text=text.replace(" ","+")
        api=requests.get(f"https://mrapiweb.ir/api/badword.php?text={text}").text
        result=json.loads(api)
        if result["isbadword"] == True:
            return True
        else:
            return False
    def randbio():
        return requests.get(f"https://mrapiweb.ir/api/bio.php").text

    def isaitext(text):
        text=text.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/aitext.php?text={text}").text
        result=json.loads(api)
        if result["aipercent"] == "0%":
            return False
        else:
            return True

    def notebook(filename,text):
        text=text.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/notebook.php?text={text}")
        with open(filename,"wb") as mr:
            mr.write(api.content)
            mr.close()
        return True
    def email(to,subject,text):
        text=text.replace(" ","+")
        subject=subject.replace(" ","+")
        requests.get(f"https://mrapiweb.ir/api/email.php?to={to}&subject={subject}&message={text}")
        return f"Email Sent To {to}"
    def ipinfo(ip):
        api=requests.get(f"https://mrapiweb.ir/api/ipinfo.php?ipaddr={ip}").text
        ip=json.loads(api)
        try:
            return ip
        except:
            raise JsonError(f"Unknown Json Key : {ip}") from None
    def arz():
        api=requests.get(f"https://mrapiweb.ir/api/arz.php").text
        arz=json.loads(api)
        try:
            return arz
        except:
            raise JsonError(f"Unknown Json Key : {ip}") from None

    def insta(link):
        return link.replace("instagram.com","ddinstagram.com")
    def voicemaker(sayas,text,filename):
        text=text.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/voice.php?sayas={sayas}&text={text}")
        with open(filename,"wb") as mr:
            mr.write(api.content)
            mr.close()
        return True
    def walletgen():
        return requests.get(f"https://mrapiweb.ir/api/walletgen.php").text
    def imagegen(text):
        global apikey
        text=text.replace(" ","-")
        return requests.get(f"https://mrapiweb.ir/api/imagegen.php?key={apikey}&imgtext={text}").text
    def proxy():
        #text=text.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/telproxy.php").text
        proxy=json.loads(api)
        return proxy["connect"]

    def fal(filename):
        api=requests.get(f"https://mrapiweb.ir/api/fal.php")
        with open(filename,"wb") as mr:
            mr.write(api.content)
            mr.close()
        return True
    def worldclock():
        return requests.get(f"https://mrapiweb.ir/api/zone.php").text

    def youtube(vid):
        global apikey
        return requests.get(f"https://mrapiweb.ir/api/yt.php?key={apikey}&id={vid}").text
    def sendweb3(privatekey,address,amount,rpc,chainid):
        return requests.get(f"https://mrapiweb.ir/api/wallet.php?key={privatekey}&address={address}&amount={amount}&rpc={rpc}&chainid={chainid}").text
    def google_drive(link):
        api=requests.get(f"https://mrapiweb.ir/api/gdrive.php?url={link}").text
        drive=json.loads(api)
        return drive["link"]
    def bing_dalle(text):
        raise EndSupport("Bing Dalle Is End Of Support") from None
    def wikipedia(text):
        return requests.get(f"https://mrapiweb.ir/wikipedia/?find={text}&lang=fa").text

    def chrome_extention(id,file):
        api = requests.get(f"https://mrapiweb.ir/api/chrome.php?id={id}").content
        with open(file,"wb") as f:
            f.write(api)
            f.close()

    def fakesite(site):
        return json.loads(requests.get(f"https://mrapiweb.ir/api/fakesite.php?site={site}").text)["is_real"]

    def webshot(site,filesave):
        global apikey
        api1 = requests.get(f"https://mrapiweb.ir/api/webshot.php?key={apikey}&url={site}&fullSize=false&height=512&width=512")
        try:
            with open(filesave,"wb") as f:
                f.write(api1.content)
                f.close()
        except:
            return api1.text
    def barcode(code):
        global apikey
        api = requests.get(f"https://mrapiweb.ir/api/barcode.php?key={apikey}&code={code}").text
        try:
            try:
                return json.loads(api)["result"]
            except:
                return json.loads(api)["message"]
        except:
            raise KeyError("API Key Not Found. Please Define API KEy By setapikey() function!. Get API Key In @mrapiweb_bot") from None
            

class hashchecker():
    def tron(thash):
        api=requests.get(f"https://mrapiweb.ir/api/cryptocheck/tron.php?hash={thash}").text
        tron=json.loads(api)
        return tron
    def tomochain(thash):
        api=requests.get(f"https://mrapiweb.ir/api/cryptocheck/tomochain.php?hash={thash}").text
        tomo=json.loads(api)
        return tomo

class fake_mail():
    def create():
        return json.loads(requests.get("https://mrapiweb.ir/api/fakemail.php?method=getNewMail").text)["results"]["email"]
    def getmails(email):
        return json.loads(requests.get(f"https://mrapiweb.ir/api/fakemail.php?method=getMessages&email={email}").text)["results"]


class tron():
    def generate():
        api=json.loads(requests.get("https://mrapiweb.ir/api/tronapi.php?action=genaddress").text)
        return api
    def balance(address):
        api=json.loads(requests.get(f"https://mrapiweb.ir/api/tronapi.php?action=getbalance&address={address}").text)
        return api["balance"]
    def info(address):
        api=json.loads(requests.get(f"https://mrapiweb.ir/api/tronapi.php?action=addressinfo&address={address}").text)
        return api
    def send(key,fromadd,to,amount):
        api=json.loads(requests.get(f"https://mrapiweb.ir/api/tronapi.php?action=sendtrx&key={key}&fromaddress={fromadd}&toaddress={to}&amount={amount}").text)
        return api
    



def help():
    return "Join @mrapilib in telegram"
