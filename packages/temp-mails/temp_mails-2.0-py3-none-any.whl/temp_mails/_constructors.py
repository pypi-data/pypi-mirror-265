from time import sleep, time
from typing import Literal
from string import ascii_lowercase, digits
import random
import json
from base64 import b64decode

import rel
import requests
from bs4 import BeautifulSoup
import websocket


def _generate_user_data(name: str=None, domain:str=None, exclude: list[str]=None, valid_domains: list[str]=None):
    """Generates a random name and domain for a given temp mail object."""
    
    name = name or "".join(random.choices(ascii_lowercase+digits, k=random.randint(8, 16)))

    valid_domains = valid_domains or valid_domains
    if domain:
        domain = domain if domain in valid_domains else random.choice(valid_domains)
    else:
        if exclude:
            valid_domains = [domain for domain in valid_domains if domain not in exclude]
        domain = random.choice(valid_domains)

    email = f"{name}@{domain}"

    return name, domain, email, valid_domains

class _WaitForMail:
    def __init__(self, indx: Literal[0, -1]):
        self.indx = indx

    def wait_for_new_email(self, delay: float=2.0, timeout: int=60):
        """
        Waits for a new mail, returns the data of the incoming email, None if timeout is hit or an error occurs\n
        Args:\n
        delay - the delay between each check in seconds\n
        timeout - the time which is allowed to pass before forcefully stopping, smaller than 0 -> no timeout
        """

        if timeout > 0: 
            start = time()
        
        old_length = len(self.get_inbox())

        while True:
            if timeout > 0 and time()-start >= timeout:
                return None
            
            if (len(data := self.get_inbox())) > old_length:
                return data[self.indx]
            
            sleep(delay)



def _deCFEmail(fp): # https://stackoverflow.com/a/58111681
    try:
        r = int(fp[:2],16)
        email = ''.join([chr(int(fp[i:i+2], 16) ^ r) for i in range(2, len(fp), 2)])
        return email
    except ValueError:
        pass


class _Livewire(_WaitForMail):
    def __init__(self, strings: dict, urls: str, order: Literal[0, -1], name: str=None, domain: str=None, exclude: list[str]=None):
        super().__init__(order)

        self.urls = urls
        self.strings = strings

        self._session = requests.Session()
        self._session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }


        # Get required data for email creation and more
        r = self._session.get(self.urls["base"])
        
        if not r.ok:
            raise Exception("Failed to create email, status", r.status_code)
        
        # Create Email
        soup = BeautifulSoup(r.text, "lxml")
        
        data = json.loads(soup.find("div", {"x-data": self.strings["first_data"]})["wire:initial-data"])

        self.valid_domains = data["serverMemo"]["data"]["domains"]
        self.name, self.domain, self.email, self.valid_domains = _generate_user_data(name, domain, exclude, self.valid_domains)
        
        self._token = soup.find("input", {"type": "hidden"})["value"]

        payload = {
            "fingerprint": data["fingerprint"],
            "serverMemo": data["serverMemo"],
            "updates": [
                {
                    "type": "fireEvent",
                    "payload": {
                        "id": "".join(random.choices(ascii_lowercase+digits, k=4)),
                        "event": "syncEmail",
                        "params": [
                            self.email
                        ]
                    }
                }
            ]
        }
                 
        r = self._session.post(self.urls["actions"], json=payload, headers={
            "x-csrf-token": self._token,
            "x-livewire": "true"
        })

        if not r.ok:
            raise Exception("Failed to create email, status", r.status_code)
        
        # Get the data required for checking messages

        data = json.loads(soup.find(self.strings["second_data"][0], {"x-data": self.strings["second_data"][1]})["wire:initial-data"])

        payload = {
            "fingerprint": data["fingerprint"],
            "serverMemo": data["serverMemo"],
            "updates": [
                {
                    "type": "fireEvent",
                    "payload": {
                        "id": "".join(random.choices(ascii_lowercase+digits, k=4)),
                        "event": "syncEmail",
                        "params": [
                            self.email
                        ]
                    }
                },
                {
                    "type": "fireEvent",
                    "payload": {
                        "id": "".join(random.choices(ascii_lowercase+digits, k=4)),
                        "event": "fetchMessages",
                        "params": []
                    }
                }
            ]
        }

        r = self._session.post(self.urls["app"], json=payload, headers={
            "x-csrf-token": self._token,
            "x-livewire": "true"
        })
        
        if not r.ok:
            raise Exception("Failed to create email, status", r.status_code)
        
        new_data = r.json()
        
        self._fingerprint = data["fingerprint"]
        self._servermemo = data["serverMemo"]
        self._servermemo["htmlHash"] = new_data["serverMemo"].get("htmlHash", data["serverMemo"]["htmlHash"]) # Tempmail.gg doesnt have it in new_data
        self._servermemo["data"].update(new_data["serverMemo"]["data"])
        self._servermemo["checksum"] = new_data["serverMemo"]["checksum"]

    def get_inbox(self) -> list[dict]:
        """
        Returns the inbox of the email as a list with mails as dicts list[dict, dict, ...]
        """

        payload = {
            "fingerprint": self._fingerprint,
            "serverMemo": self._servermemo,
            "updates": [
                {
                    "type": "fireEvent",
                    "payload": {
                        "id": "".join(random.choices(ascii_lowercase+digits, k=4)),
                        "event": "fetchMessages",
                        "params": []
                    }
                }
            ]
        }

        r = self._session.post(self.urls["app"], json=payload, headers={
            "x-csrf-token": self._token,
            "x-livewire": "true"
        })
        
        if r.ok:
            data = r.json()
            return [
                {
                    "id": email["id"],
                    "time": email["date"],
                    "subject": email["subject"],
                    "content": email["content"]
                } 
                for email in data["serverMemo"]["data"]["messages"]
            ] if ("data" in data["serverMemo"] and not "error" in data["serverMemo"]["data"]) else []


class _Livewire2(_WaitForMail):
    def __init__(self, strings: dict, urls: str, order: Literal[0, -1], name: str=None, domain: str=None, exclude: list[str]=None):
        super().__init__(order)

        self.urls = urls
        self.strings = strings

        self._session = requests.Session()
        self._session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }


        r = self._session.get(self.urls["base"])

        
        if not r.ok:
            raise Exception("Failed to create email, status", r.status_code)
        
        soup = BeautifulSoup(r.text, "lxml")
        
        data = json.loads(soup.find("div", {"x-data": self.strings["first_data"]})["wire:initial-data"])

        self.valid_domains = data["serverMemo"]["data"]["domains"]
        self.name, self.domain, self.email, self.valid_domains = _generate_user_data(name, domain, exclude, self.valid_domains)
        self._token = soup.find("input", {"type": "hidden"})["value"]

        
        # prepare email creation
        payload = {
            "fingerprint": data["fingerprint"],
            "serverMemo": data["serverMemo"],
            "updates": [
                {
                    "type": "syncInput",
                    "payload": {
                        "id": "".join(random.choices(ascii_lowercase+digits, k=4)),
                        "name": "user",
                        "value": self.name
                    }
                },
                {
                    "type": "callMethod",
                    "payload": {
                        "id": "".join(random.choices(ascii_lowercase+digits, k=4)),
                        "method": "setDomain",
                        "params": [
                            self.domain
                        ]
                    }
                }
            ]
        }
        
        r = self._session.post(self.urls["actions"], json=payload, headers={
            "x-csrf-token": self._token,
            "x-livewire": "true"
        })

        if not r.ok:
            raise Exception("Failed to create email, status", r.status_code)
        
        # create email
        data = r.json()
        payload["serverMemo"]["data"].update(data["serverMemo"]["data"])
        payload["updates"] = [
            {
                "type": "callMethod",
                "payload": {
                    "id": "fhdk",
                    "method": "create",
                    "params": []
                }
            }
        ]
        payload["serverMemo"]["checksum"] = data["serverMemo"]["checksum"]
        
        r = self._session.post(self.urls["actions"], json=payload, headers={
            "x-csrf-token": self._token,
            "x-livewire": "true"
        })
        if not r.ok:
            raise Exception("Failed to create email, status", r.status_code)
        
        # continue with next steps as usual
        r = self._session.get(self.urls["mailbox"])
        if not r.ok:
            raise Exception("Failed to create email, status", r.status_code)
        
        soup = BeautifulSoup(r.text, "lxml")
        data = json.loads(soup.find("div", {"x-data": self.strings["first_data2"]})["wire:initial-data"])

        payload = {
            "fingerprint": data["fingerprint"],
            "serverMemo": data["serverMemo"],
            "updates": [
                {
                    "type": "fireEvent",
                    "payload": {
                        "id": "".join(random.choices(ascii_lowercase+digits, k=4)),
                        "event": "syncEmail",
                        "params": [
                            self.email
                        ]
                    }
                }
            ]
        }

        r = self._session.post(self.urls["actions"], json=payload, headers={
            "x-csrf-token": self._token,
            "x-livewire": "true"
        })
        if not r.ok:
            raise Exception("Failed to create email, status", r.status_code)
        
        data = json.loads(soup.find("main", {"x-data": self.strings["second_data"]})["wire:initial-data"])

        payload = {
            "fingerprint": data["fingerprint"],
            "serverMemo": data["serverMemo"],
            "updates": [
                {
                    "type": "fireEvent",
                    "payload": {
                        "id": "".join(random.choices(ascii_lowercase+digits, k=4)),
                        "event": "syncEmail",
                        "params": [
                            self.email
                        ]
                    }
                },
                {
                    "type": "fireEvent",
                    "payload": {
                        "id": "".join(random.choices(ascii_lowercase+digits, k=4)),
                        "event": "fetchMessages",
                        "params": []
                    }
                }
            ]
        }

        r = self._session.post(self.urls["app"], json=payload, headers={
            "x-csrf-token": self._token,
            "x-livewire": "true"
        })
        
        if not r.ok:
            raise Exception("Failed to create email, status", r.status_code)
        
        new_data = r.json()
        
        self._fingerprint = data["fingerprint"]
        self._servermemo = data["serverMemo"]
        self._servermemo["htmlHash"] = new_data["serverMemo"].get("htmlHash", data["serverMemo"]["htmlHash"]) # Tempmail.gg doesnt have it in new_data
        self._servermemo["data"].update(new_data["serverMemo"]["data"])
        self._servermemo["checksum"] = new_data["serverMemo"]["checksum"]


    def get_inbox(self) -> list[dict]:
        """
        Returns the inbox of the email as a list with mails as dicts list[dict, dict, ...]
        """

        payload = {
            "fingerprint": self._fingerprint,
            "serverMemo": self._servermemo,
            "updates": [
                {
                    "type": "fireEvent",
                    "payload": {
                        "id": "".join(random.choices(ascii_lowercase+digits, k=4)),
                        "event": "fetchMessages",
                        "params": []
                    }
                }
            ]
        }

        r = self._session.post(self.urls["app"], json=payload, headers={
            "x-csrf-token": self._token,
            "x-livewire": "true"
        })
        
        if r.ok:
            data = r.json()
            return [
                {
                    "id": email["id"],
                    "time": email["date"],
                    "subject": email["subject"],
                    "content": email["content"]
                } 
                for email in data["serverMemo"]["data"]["messages"]
            ] if ("data" in data["serverMemo"] and not "error" in data["serverMemo"]["data"]) else []



class _Tenminemail_Tempailorg(_WaitForMail):
    def __init__(self, urls: dict):
        """
        Generate a random inbox
        """
        
        super().__init__(-1)
        self.urls = urls

        self._session = requests.Session()
        
        self._session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

        r = self._session.post(self.urls["mailbox"])

        if not r.ok:
            raise Exception("Failed to create email, status", r.status_code)
        
        data = r.json()

        self.email: str = data["mailbox"]
        self.name, self.domain = self.email.split("@", maxsplit=1)

        self._token = data["token"]
        self._session.headers["Authorization"] = "Bearer " + self._token


    def get_inbox(self) -> list[dict]:
        """
        Returns the inbox of the email as a list with mails as dicts list[dict, dict, ...], None if failure
        """

        r = self._session.get(self.urls["messages"])
        
        if r.ok:
            return r.json()["messages"]

    
    def get_mail_content(self, mail_id: str) -> dict:
        """
        Returns the whole content of a mail\n
        mail_id - id of the message
        """
    
        r = self._session.get(self.urls["messages"]+mail_id)
        
        if r.ok:
            return r.json()



class _Minuteinbox_Disposablemail_Fakemail(_WaitForMail):
    def __init__(self, base_url: str):
        """
        Generate a random inbox
        """
        
        super().__init__(0)
        self.base_url = base_url

        self._session = requests.Session()
        
        self._session.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
    
        r = self._session.get(base_url+"/index/index")

        if not r.ok:
            raise Exception("Failed to create email, status", r.status_code)
        
        data = json.loads(r.content.decode("utf-8-sig"))

        self.email: str = data["email"]
        self.name, self.domain = self.email.split("@", maxsplit=1)


    def get_mail_content(self, mail_id: str | int) -> str:
        """
        Returns the whole content of a mail\n
        mail_id - id of the message\n
        returns the html of the content as a string
        """
    
        r = self._session.get(f"{self.base_url}/email/id/{mail_id}")
        if r.ok:
            return r.text.split("\n", maxsplit=1)[1]


    def get_inbox(self) -> list[dict]:
        """
        Returns the inbox of the email as a list with mails as dicts list[dict, dict, ...]
        """

        r = self._session.get(self.base_url+"/index/refresh")
        
        if r.ok:
            # the names of the variables are really fucked so we reformat them
            
            resp = json.loads(r.content.decode("utf-8-sig"))
            data = []
            
            for mail in resp:
                data.append({
                    "id": mail["id"],
                    "time": mail["kdy"],
                    "from": mail["od"],
                    "subject": mail["predmet"]
                })
            
            return data



class _Mailcare(_WaitForMail):
    def __init__(self, base_url: str, name: str=None, domain:str=None, exclude: list[str]=None):
        """
        Generate an inbox\n
        Args:\n
        name - name for the email, if None a random one is chosen\n
        domain - the domain to use, domain is prioritized over exclude\n
        exclude - a list of domain to exclude from the random selection\n
        """

        super().__init__(0)
        self.base_url = base_url

        self._session = requests.Session()
        
        self.name, self.domain, self.email, self.valid_domains = _generate_user_data(name, domain, exclude, self.get_valid_domains())
    
    
    def get_mail_content(self, mail_id: str) -> str:
        """
        Returns the content of a given mail_id as a html string\n
        Args:\n
        mail_id - the id of the mail you want the content of
        """

        r = self._session.get(f"{self.base_url}/api/emails/{mail_id}", headers={"Accept": "text/html,text/plain"})
        if r.ok:
            return r.text.split("</a><br>", maxsplit=1)[1] # remove ad


    def get_inbox(self) -> list[dict]:
        """
        Returns the inbox of the email as a list with mails as dicts list[dict, dict, ...], None if failure
        """
        
        r = self._session.get(f"{self.base_url}/api/emails?inbox={self.email}")
        
        if r.status_code == 404:
            return []
        if r.ok:
            return r.json()["data"]



class _Tmailor_Tmail_Cloudtempmail:

    def __init__(self, host: Literal["https://tmailor.com/", "https://tmail.ai/", "https://cloudtempmail.com/"]):
        """
        Generate a random inbox
        """
        # pertera.com,ipxwan.com,x1ix.com,1sworld.com,videotoptop.com,bookgame.org,likemovie.net,s3k.net,mp3oxi.com,cloudtempmail.net,nextsuns.com,aluimport.com,happy9toy.com,leechchannel.com

        self._session = requests.Session()
        
        r = self._session.get(host)
       
        if not r.ok:
            raise Exception("Failed to create email, status", r.status_code)

        self.link = r.text.split('web_graph="', maxsplit=1)[1].split('"', maxsplit=1)[0]
        
        r = self._session.post(self.link+"/email/wtf", data={"type": "newemail"})
        if not r.ok:
            raise Exception("Failed to create email, status", r.status_code)
        
        data = r.json()
        
        if data["msg"] == "actionblock":
            raise Exception("Ratelimited")

        self.email_data = {
            "email": data["email"],
            "create": data["create"],
            "sort": data["sort"],
            "add": data["create"],
            "accesstoken": data["accesstoken"]
        }
        
        self.email = data["email"]
        self.name, self.domain = self.email.split("@", maxsplit=1)

        # register the email
        def on_message(ws, message: str):
            message = json.loads(message)
            
            if message["msg"] == "welcome":
                ws.send(json.dumps({
                    "action": "newemail",
                    "accesstokenx": "",
                    "accesstoken": self.email_data["accesstoken"]
                }))
                ws.close()

        ws = websocket.WebSocketApp("wss" + self.link.removeprefix("https") +"/wss", on_message=on_message)
        ws.run_forever()


    def get_mail_content(self, mail_id: str) -> str:
        """
        Returns the content of a given mail_id\n
        Args:\n
        mail_id - the id of the mail you want the content of
        """
        
        def on_open(ws):
            ws.send(json.dumps({
                    "action": "read",
                    "email": self.email,
                    "accesstoken": self.email_data["accesstoken"],
                    "email_id": mail_id
            }))

        def on_message(ws, message: str):
            message = json.loads(message)
            
            if message["msg"] == "welcome":        
                ws.send(json.dumps({
                    'email': self.email, 
                    'create': self.email_data["create"], 
                    'sort': self.email_data["sort"], 
                    'add': self.email_data["sort"], 
                    'accesstoken': self.email_data["accesstoken"]
                }))

            elif message["msg"] == "updateinbox":
                nonlocal email_data
                
                if message["lists"]:
                    email_data = b64decode(message["lists"][0]["content"]).decode()
                
                ws.close()

        email_data = None

        ws = websocket.WebSocketApp("wss" + self.link.removeprefix("https") +"/wss", on_message=on_message, on_open=on_open)
        ws.run_forever()
        
        return email_data


    def get_inbox(self) -> list[dict]:
        """
        Returns the inbox of the email as a list with mails as dicts list[dict, dict, ...]\n
        """

        def on_message(ws, message: str):
            message = json.loads(message)
            
            if message["msg"] == "welcome":
                ws.send(json.dumps({
                    'email': self.email, 
                    'create': self.email_data["create"], 
                    'sort': self.email_data["sort"], 
                    'add': self.email_data["sort"], 
                    'accesstoken': self.email_data["accesstoken"]
                }))

            elif message["msg"] == "ok":
                nonlocal email_data
                email_data = []
                
                if message["lists"]:
                    for email in message["lists"]:
                        email_data.append({
                            "id": email["email_id"],
                            "subject": email["subject"],
                            "from": email["sender_email"],
                            "time": email["receive_time"],
                        })
                
                ws.close()

        email_data = None

        ws = websocket.WebSocketApp("wss" + self.link.removeprefix("https") +"/wss", on_message=on_message)
        ws.run_forever()
        
        return email_data
        

    def wait_for_new_email(self, delay: None=None, timeout: int=60) -> dict:
        """
        Waits for a new mail (using websockets), returns the data of the incoming email, None if timeout is hit or an error occurs\n
        Args:\n
        timeout - the time which is allowed to pass before forcefully stopping, <=0 -> no timeout. Note that it does not stop at exactly the time due to being sync
        delay - not used
        """

        if timeout > 0: 
            start = time()

        def on_message(ws, message: str):
            nonlocal new_msg
            message = json.loads(message)
            
            match message["msg"]:
                case "welcome":
                    ws.send(json.dumps({
                        'email': self.email, 
                        'create': self.email_data["create"], 
                        'sort': self.email_data["sort"], 
                        'add': self.email_data["sort"], 
                        'accesstoken': self.email_data["accesstoken"]
                    }))

                case "ok":
                    self.email_data["client_key"] = message["client_key"]
                    
                    nonlocal email_data
                    if new_msg:
                        email_data = message["lists"][0]
                        email_data = {
                            "id": email_data["email_id"],
                            "subject": email_data["subject"],
                            "from": email_data["sender_email"],
                            "time": email_data["receive_time"],
                        }
                        rel.abort()

                case "checkmailnow":
                    ws.send(json.dumps(self.email_data))
                    new_msg = True

            if timeout > 0 and time()-start >= timeout:
                rel.abort()


        def on_error(ws, error):
            if timeout > 0 and time()-start >= timeout:
                rel.abort()

        email_data = None
        new_msg = False

        ws = websocket.WebSocketApp("wss" + self.link.removeprefix("https") +"/wss", on_message=on_message, on_error=on_error)
        ws.run_forever(ping_interval=15, ping_payload="ping", dispatcher=rel)
        rel.dispatch()
        
        return email_data



class _Tenminutesemail_Eztempmail_Tmailgg(_WaitForMail):
    def __init__(self, base_url: str, name: str=None, domain: str=None, exclude: list[str]=None):

        super().__init__(0)

        self.base_url = base_url.removesuffix("/")
        self._session = requests.Session()
        
        self._session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
    
        r = self._session.get(self.base_url)
        
        if r.status_code == 403:
            raise Exception(f"Error, you are ratelimited on {self.base_url}, please wait.")       
        if not r.ok:
            raise Exception("Failed to create email, status", r.status_code)
        if "Bot Verification" in r.text:
            raise Exception(f"Error, you need to verify Captcha manually on {self.base_url}.") 

        self._token = BeautifulSoup(r.text, "lxml").find("meta", {"name": "csrf-token"})["content"]
        
        r = self._session.post(self.base_url+"/messages", data={
            "_token": self._token,
            "captcha": ""
        })

        if not r.ok:
            raise Exception("Failed to create email, status", r.status_code)
        
        if not domain and not name and not exclude:    
            data = r.json()
            self.email: str = data["mailbox"]
            self.name, self.domain = self.email.split("@", maxsplit=1)
        
        else:
            self.name, self.domain, self.email, self.valid_domains = _generate_user_data(name, domain, exclude, self.get_valid_domains())
            
            r = self._session.post(self.base_url+"/create", data={
                "_token": self._token,
                "name": self.name,
                "domain": self.domain
            })
            if not r.ok:
                raise Exception(f"Something went wrong on Email Creation, status: {r.status_code}, response content:\n{r.text}")
            
            r = self._session.post(self.base_url+"/messages", data={
                "_token": self._token,
                "captcha": ""
            })    
            if not r.ok:
                raise Exception("Failed to create email, status", r.status_code)
            
            data = r.json()
            self.email: str = data["mailbox"]
            self.name, self.domain = self.email.split("@", maxsplit=1)


    def get_inbox(self) -> list[dict]:
        """
        Returns the inbox of the email as a list with mails as dicts list[dict, dict, ...]
        """

        r = self._session.post(self.base_url+"/messages", data={
            "_token": self._token,
            "captcha": ""
        })
        
        if r.ok:
            return [{
                "id": email["id"],
                "time": email["receivedAt"],
                "subject": email["subject"],
                "content": email["content"]
            } for email in r.json()["messages"]] 
        

class _Tempail_Tempmailnet:
    def __init__(self, base_url: str, offset_of_email_content: int=0):
        """
        Generate a random inbox
        """
        # offset_of_email_content - tempmail.net also adds another script before the cloudflare script in the mail content, so we remove that in the end

        self.base_url = base_url.removesuffix("/")
        self.offset_of_email_content = offset_of_email_content

        self._session = requests.Session()

        r = self._session.get(self.base_url)
        if not r.ok:
            raise Exception("Failed to create email, status:", r.status_code)
        if "Verifying your request, please wait..." in r.text:
            raise Exception("Error, you need to verify Captcha manually on "+self.base_url)
        
        soup = BeautifulSoup(r.text, "lxml")
        self.email = soup.find("input", {"id": "eposta_adres"})["value"]
        data = soup.find("script").text.split('var oturum="', maxsplit=1)[1]
        self._some_val = data.split('"', maxsplit=1)[0]
        self._time = data.split('var tarih="', maxsplit=1)[1].split('"', maxsplit=1)[0]


    def get_inbox(self) -> list[dict]:
        """
        Returns the inbox of the email as a list with mails as dicts list[dict, dict, ...]
        """

        r = self._session.get(self.base_url)
        if not r.ok:
            return None
        if "Verifying your request, please wait..." in r.text:
            raise Exception("Error, you need to verify Captcha manually on "+self.base_url)
        
        soup = BeautifulSoup(r.text, "lxml")

        return [{
            "id": email["id"],
            "from": _deCFEmail(email.find("div", {"class": "gonderen"}).span["data-cfemail"]),
            "subject": email.find("div", {"class": "baslik"}).text,
            "time": email.find("div", {"class": "zaman"}).text
        } for email in soup.find_all("li", {"class": "mail"})]
            

    def get_mail_content(self, mail_id: str) -> str:
        """
        Returns the whole content of a mail as a html string\n
        mail_id - id of the message
        """
        
        r = self._session.get(self.base_url+"/"+mail_id)
        if not r.ok:
            return None
        if "Verifying your request, please wait..." in r.text:
            raise Exception("Error, you need to verify Captcha manually on "+self.base_url)

        r = self._session.get(BeautifulSoup(r.text, "lxml").find("div", {"class": "mail-oku-panel"}).iframe["src"])
        if not r.ok:
            return None
        if "Verifying your request, please wait..." in r.text:
            raise Exception("Error, you need to verify Captcha manually on "+self.base_url)

        soup = BeautifulSoup(r.text, "lxml")
        
        google_translate_script = soup.find('script', {'type': 'text/javascript', 'src': '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit'})
        cloudflare_script = soup.find('script', {'data-cfasync': 'false'})
        elements_between_scripts = google_translate_script.find_next_siblings()

        elements = []
        for element in elements_between_scripts:
            if element == cloudflare_script:
                break
            elements.append(str(element))
        return "\n".join(elements[:-self.offset_of_email_content]) if self.offset_of_email_content != 0 else "\n".join(elements)


    def wait_for_new_email(self, delay: float=2.0, timeout: int=60):
        """
        Waits for a new mail, returns the data of the incoming email, None if timeout is hit or an error occurs\n
        Args:\n
        delay - the delay between each check in seconds\n
        timeout - the time which is allowed to pass before forcefully stopping, smaller than 0 -> no timeout
        """
        if timeout > 0: 
            start = time()
        

        while True:
            if timeout > 0 and time()-start >= timeout:
                return None
            
            r = self._session.post(self.base_url+"/en/api/kontrol/", data={
                "oturum": self._some_val,
                "tarih": self._time,
                "geri_don": self.base_url
            })
            
            if not r.ok:
                return None
            
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "lxml")
                self._time = soup.find("script").text.split('tarih="', maxsplit=1)[1].split('"', maxsplit=1)[0]
                email = soup.find("li", {"class": "mail"})
                return {
                    "id": email["id"],
                    "from": _deCFEmail(email.find("div", {"class": "gonderen"}).span["data-cfemail"]),
                    "subject": email.find("div", {"class": "baslik"}).text,
                    "time": email.find("div", {"class": "zaman"}).text
                }

            sleep(delay)
