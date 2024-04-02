from time import time

import json

import rel
import requests
import websocket

from ._constructors import _generate_user_data

class Tempmail_ninja():
    """An API Wrapper around the https://tempmail.ninja/ website"""

    def __init__(self, name: str=None, domain:str=None, exclude: list[str]=None):
        """
        Generate an inbox\n
        Args:\n
        name - name for the email, if None a random one is chosen\n
        domain - the domain to use, domain is prioritized over exclude\n
        exclude - a list of domain to exclude from the random selection\n
        """

        self._session = requests.Session()
        
        # for IDE
        self.name: str
        self.domain: str
        self.email: str
        self.valid_domains: str

        def on_message(ws, msg):
            if msg.startswith("0"): # connected
                ws.send("40")

            elif msg.startswith("2"): # ping
                ws.send("3")

            elif msg.startswith("40"): # gets send out at the beginning
                ws.send('42["get_domains"]')

            elif msg.startswith("42"):
                data = json.loads(msg[2:])
                
                if data[0] == "set_domains_data":
                    self.name, self.domain, self.email, self.valid_domains = _generate_user_data(name, domain, exclude, [domain["name"] for domain in data[1]])
                    payload = "42"+ json.dumps(["get_email_data",{"action":"create","data":{"email_alias":self.name,"email_domain":self.domain}}])
                    ws.send(payload)

                elif data[0] == "actions_for_created_email": # email created
                    rel.abort()

                elif data[0] == "enable_active_form" or (data[0] == "show_alert" and data[1]["message"] in ("The tempmail is invalid.", f"The {self.domain} emails have expired. You cannot continue to use them.")):
                    raise Exception("Failed to create email, invalid email")

        
        ws = websocket.WebSocketApp("wss://websocket.solucioneswc.com/socket.io/?EIO=4&transport=websocket", 
                                    on_close=lambda *args: rel.abort(), on_error=lambda *args: rel.abort(), on_message=on_message, 
                                    header={"Origin": "https://tempmail.ninja"}
                                    )
        ws.run_forever(suppress_origin=True, dispatcher=rel)
        rel.dispatch()


    @staticmethod
    def get_valid_domains() -> list[str]:
        """
        Returns a list of valid domains of the service (format: abc.xyz) as a list.\n
        It is prefered if you use the valid_domains list of an already initialised mail object.
        """
        
        def on_message(ws, msg):
            if msg.startswith("0"): # connected
                ws.send("40")

            elif msg.startswith("2"): # ping
                ws.send("3")

            elif msg.startswith("40"): # gets send out at the beginning
                ws.send('42["get_domains"]')

            elif msg.startswith("42"):
                data = json.loads(msg[2:])
                
                if data[0] == "set_domains_data":
                    nonlocal valid_domains
                    valid_domains = [domain["name"] for domain in data[1]]
                    rel.abort()
        
        valid_domains = None
        ws = websocket.WebSocketApp("wss://websocket.solucioneswc.com/socket.io/?EIO=4&transport=websocket", 
                                    on_close=lambda *args: rel.abort(), on_error=lambda *args: rel.abort(), on_message=on_message, 
                                    header={"Origin": "https://tempmail.ninja"}
                                    )
        ws.run_forever(suppress_origin=True, dispatcher=rel)
        rel.dispatch()
        return valid_domains


    def get_mail_content(self, mail_id: str):
        """
        Returns the content of a given mail_id as a html string\n
        Args:\n
        mail_id - the id of the mail you want the content of
        """

        def on_message(ws, msg):
            if msg.startswith("0"): # connected
                ws.send("40")

            elif msg.startswith("2"): # ping
                ws.send("3")

            elif msg.startswith("40"):
                ws.send("42"+json.dumps([
                    "get_email_message",
                    {
                        "email_address": self.email,
                        "email_message_id": mail_id,
                        "email_message_type": "inbound"
                    }
                ]))
            
            elif msg.startswith("42"):
                data = json.loads(msg[2:])
    
                if data[0] == "open_message":
                    nonlocal email_data
                    email_data = data[1]["email_message_data"]["data"]["content"]
                    rel.abort()

        email_data = None
        ws = websocket.WebSocketApp(f"wss://websocket.solucioneswc.com/socket.io/?email_address={self.email}&email_password=&email_alias={self.name}&email_domain={self.domain}&message_id=null&page_type=inbox&EIO=4&transport=websocket", 
                                    on_close=lambda *args: rel.abort(), on_error=lambda *args: rel.abort(), on_message=on_message, 
                                    header={"Origin": "https://tempmail.ninja"}
                                    )
        ws.run_forever(suppress_origin=True, dispatcher=rel)
        rel.dispatch()
        return email_data


    def get_inbox(self, return_content: bool=True) -> list[dict]:
        """
        Returns the inbox of the email as a list with mails as dicts list[dict, dict, ...]\n
        return_content - if the returned data should contain the content. If false we would need to create a new websocket connection to get the content. Not recommended if you have lots of emails and only want the content of some of them.
        """
        
        def on_message(ws, msg):
            if msg.startswith("0"): # connected
                ws.send("40")

            elif msg.startswith("2"): # ping
                ws.send("3")
            
            elif msg.startswith("42"):
                data = json.loads(msg[2:])
    
                if data[0] == "insert_email_messages":
                    nonlocal email_data
                    if return_content: nonlocal content_count
                    
                    email_data = [{
                        "id": str(email["id"]),
                        "time": email["date"],
                        "from": email["sender"]["text"],
                        "subject": email["subject"]
                    } for email in data[1]["email_messages"]]
                    
                    if not return_content or len(email_data) == 0:
                        rel.abort()

                    for email in email_data:
                        ws.send("42"+json.dumps([
                        "get_email_message",
                        {
                            "email_address": self.email,
                            "email_message_id": email["id"],
                            "email_message_type": "inbound"
                        }
                    ]))
                
                elif data[0] == "open_message": # only happens after insert_email_messages and if return_content is true so we can assume email_data and content_count exists
                    content_count+=1
                    for email in email_data:
                        if str(data[1]["email_message_data"]["id"]) == email["id"]:
                            email["content"] = data[1]["email_message_data"]["data"]["content"]
                            break
                    
                    if content_count == len(email_data):
                        rel.abort()

        email_data = None
        if return_content: content_count = 0
        
        ws = websocket.WebSocketApp(f"wss://websocket.solucioneswc.com/socket.io/?email_address={self.email}&email_password=&email_alias={self.name}&email_domain={self.domain}&message_id=null&page_type=inbox&EIO=4&transport=websocket", 
                                    on_close=lambda *args: rel.abort(), on_error=rel.abort(), on_message=on_message, 
                                    header={"Origin": "https://tempmail.ninja"}
                                    )
        ws.run_forever(suppress_origin=True, dispatcher=rel)
        rel.dispatch()
        return email_data
        

    def wait_for_new_email(self, delay: float=2.0, timeout: int=60, return_content: bool=True):
        """
        Waits for a new mail (using websockets), returns the data of the incoming email, None if timeout is hit or an error occurs\n
        Args:\n
        timeout - the time which is allowed to pass before forcefully stopping, <=0 -> no timeout. Note that it does not stop at exactly the time due to being sync
        delay - not used, simply for compatability\n
        return_content - if the returned data should contain the content. If false we would need to create a new websocket connection to get the content.
        """

        start = time()
        
        def on_message(ws, msg):
            
            if msg.startswith("0"): # connected
                ws.send("40")

            elif msg.startswith("2"): # ping
                ws.send("3")

            elif msg.startswith("42"):
                data = json.loads(msg[2:])
                
                if data[0] == "new_message_notify":
                    nonlocal email_data
                    email_data = {
                        "id": str(data[1]["email_message"]["id"]),
                        "time": data[1]["email_message"]["date"],
                        "from": data[1]["email_message"]["sender"]["text"],
                        "subject": data[1]["email_message"]["subject"]
                    }
                    if not return_content:
                        rel.abort()
                    
                    ws.send("42"+json.dumps([
                        "get_email_message",
                        {
                            "email_address": self.email,
                            "email_message_id": email_data["id"],
                            "email_message_type": "inbound"
                        }
                    ]))

                elif data[0] == "open_message": # only happens after new_message_notify so we can assume email_data exists
                    email_data["content"] = data[1]["email_message_data"]["data"]["content"]
                    rel.abort()

            if timeout > 0 and time()-start >= timeout:
                rel.abort()

        email_data = None
        ws = websocket.WebSocketApp(f"wss://websocket.solucioneswc.com/socket.io/?email_address={self.email}&email_password=&email_alias={self.name}&email_domain={self.domain}&message_id=null&page_type=inbox&EIO=4&transport=websocket", 
                                    on_close=lambda *args: rel.abort(), on_error=lambda *args: rel.abort(), on_message=on_message, 
                                    header={"Origin": "https://tempmail.ninja"}
                                    )
        ws.run_forever(suppress_origin=True, dispatcher=rel)
        rel.dispatch()
        return email_data
    