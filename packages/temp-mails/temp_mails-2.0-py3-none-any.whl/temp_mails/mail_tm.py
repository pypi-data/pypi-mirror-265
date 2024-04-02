import random
from string import ascii_lowercase, digits
import json

import requests

from ._constructors import _generate_user_data

class Mail_tm():
    """An API Wrapper around the https://mail.tm/ website"""

    def __init__(self, name: str=None, domain:str=None, exclude: list[str]=None, password: str=None):
        """
        Generate an inbox\n
        Args:\n
        name - name for the email, if None a random one is chosen\n
        domain - the domain to use, domain is prioritized over exclude\n
        exclude - a list of domain to exclude from the random selection\n
        password - a password used for authentification
        """
        
        self._session = requests.Session()
        
        self._session.headers = {
            "accept": "application/ld+json",
            "Content-Type": "application/json",
        }

        self.password = password or "".join(random.choices(ascii_lowercase+digits, k=random.randint(8, 16)))

        self.name, self.domain, self.email, self.valid_domains = _generate_user_data(name, domain, exclude, self.get_valid_domains())
        
        r = self._session.post("https://api.mail.tm/accounts", json={
            "address": self.email,
            "password": self.password
        })

        if not r.ok:
            raise Exception("Failed to create account, status: ", r.status_code) 
       
        data = r.json()
        self.email = data["address"]
        self._id = data["id"]

        r = self._session.post("https://api.mail.tm/token", json={
            "address": self.email,
            "password": self.password
        })
        
        if not r.ok:
            raise Exception("Failed to create account, status: ", r.status_code)
        
        data = r.json()
        self._token = data["token"]
        self._session.headers["Authorization"] = "Bearer " + self._token


    @staticmethod
    def get_valid_domains() -> list[str]:
        """
        Returns a list of valid domains of the service (format: abc.xyz) as a list
        """
        
        r = requests.get("https://api.mail.tm/domains")
        if r.ok:
            return [domain["domain"] for domain in r.json()["hydra:member"]]  


    def get_mail_content(self, mail_id: str) -> str:
        """
        Returns the content of a given mail_id\n
        Args:\n
        mail_id - the id of the mail you want the content of
        """

        r = self._session.get("https://api.mail.tm/messages/"+mail_id)
        if r.ok:
            data = r.json()
            return data["html"][0]


    def get_inbox(self) -> list[dict]:
        """
        Returns the inbox of the email as a list with mails as dicts list[dict, dict, ...], None if failure
        """
        
        r = self._session.get("https://api.mail.tm/messages")
        if r.ok:
            return [
                {
                    "id": msg["id"],
                    "from": msg["from"]["address"],
                    "subject": msg["subject"],
                    "time": msg["createdAt"]
                } 
                for msg in r.json()["hydra:member"]
           ]

    
    def wait_for_new_email(self, delay: None=None, timeout: int=60) -> dict:
        """
        Waits for a new mail (using event streams), returns the data of the incoming email, None if timeout is hit or an error occurs\n
        Args:\n
        timeout - the time which is allowed to pass before forcefully stopping, <=0 -> no timeout. Note that it does not stop at exactly the time due to being sync
        delay - not used, simply for compatability
        """
        
        try:
            eoc = b"\n\n"
            chunk = b""
            for r in self._session.get("https://mercure.mail.tm/.well-known/mercure?topic=/accounts/"+self._id, 
                headers={
                    "Accept": "text/event-stream",
                }, 
                stream=True, 
                timeout=timeout
            ):
                chunk += r
                if r.endswith(eoc): # Complete chunk of datareceived
                    for data in chunk.splitlines():
                        if data.startswith(b'data: {"@context":"/contexts/Message'):
                            msg = json.loads(data[6:].decode())
                            return {
                                "id": msg["id"],
                                "from": msg["from"]["address"],
                                "subject": msg["subject"],
                                "time": msg["createdAt"]
                            }

                    chunk = b""

        except requests.exceptions.ConnectionError:
            return None
