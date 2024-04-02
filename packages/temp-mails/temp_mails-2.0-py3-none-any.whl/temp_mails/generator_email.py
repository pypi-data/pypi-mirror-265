from time import sleep, time
import json
import requests
from bs4 import BeautifulSoup
import websocket

from ._constructors import _generate_user_data

class Generator_email():
    """An API Wrapper around the https://generator.email/ website"""

    def __init__(self, name: str=None, domain:str=None, exclude: list[str]=None):
        """
        Generate an inbox\n
        Args:\n
        name - name for the email, if None a random one is chosen\n
        domain - the domain to use, domain is prioritized over exclude. There is no validation for the domain\n
        exclude - a list of domain to exclude from the random selection\n
        """

        self._session = requests.Session()

        self.name, self.domain, self.email, self.valid_domains = _generate_user_data(name, domain, exclude, self.get_valid_domains())

    @staticmethod
    def get_valid_domains() -> list[str]:
        """
        Returns a list of valid domains of the service (format: abc.xyz) as a list.\nThis is not a complete list but a random selection.
        """

        r = requests.get("https://generator.email/")
        if r.ok:
            soup = BeautifulSoup(r.text, "lxml")
            return [domain.text for domain in soup.find_all("div", {"class": "e7m tt-suggestion"})]
        

    def get_mail_content(self, mail_id: str, retry: bool=True, retry_delay: int=1, max_retries: int=3, _retries: int=1) -> dict:
        """
        Returns the content of a given mail_id as a BeautifulSoup html object\n
        Args:\n
        mail_id - the id of the mail you want the content of
        """

        try:
            r = self._session.get(f"https://generator.email/{self.domain}/{self.name}/{mail_id}")
        except requests.exceptions.ConnectionError:
            if retry:
                if _retries == max_retries:
                    return None

                sleep(retry_delay)
                return self.get_mail_content(mail_id=mail_id, retry=retry, retry_delay=retry_delay, _retries=_retries+1)

        if r.ok:
            soup = BeautifulSoup(r.text, "lxml")
            email_list = soup.find("div", {"id": "email-table"})

            return email_list.find("div", {"class": "e7m mess_bodiyy"})
        
    def get_inbox(self, retry: bool=True, retry_delay: int=1, max_retries: int=3, _retries: int=1) -> list[dict]:
        """
        Returns the inbox of the email as a list with mails as dicts list[dict, dict, ...], None if failure. If there is 1 email in the inbox, it also returns the content of the email as a BeautifulSoup object. If there are more than 1 email in the inbox, it returns the ids of the emails, but no content\n
        retry - retry if the site refuses to allow a connection (does that sometimes, maybe ratelimit)\n
        retry_delay - how long to wait before a retry\n
        max_retries - how many retries to allow before stopping\n
        """

        try:
            r = self._session.get(f"https://generator.email/{self.domain}/{self.name}")
        except requests.exceptions.ConnectionError:
            if retry:
                if _retries == max_retries:
                    return None

                sleep(retry_delay)
                return self.get_inbox(retry=retry, retry_delay=retry_delay, _retries=_retries+1)
        
        if r.ok:
            soup = BeautifulSoup(r.text, "lxml")
            
            email_list = soup.find("div", {"id": "email-table"})
            if not email_list:
                return []
            
            # if there is one email, the whole structure is different, if there are more, there is an href for each email
            if soup.find("span", {"id": "mess_number"}).text == "1": 
                email_data = email_list.find("div", {"class": "e7m list-group-item list-group-item-info"})
                data = {
                    "from": email_data.find("div", {"class": "e7m from_div_45g45gg"}).text,
                    "subject": email_data.find("div", {"class": "e7m subj_div_45g45gg"}).text,
                    "time": email_data.find("div", {"class": "e7m time_div_45g45gg"}).text,
                    "content": email_list.find("div", {"class": "e7m mess_bodiyy"})
                }

                return [data] 
            
            emails = []
            for email in email_list.findChildren("a"):
                data = {
                    "id": email["href"].rsplit("/", maxsplit=1)[1],
                    "from": email.find("div", {"class": "e7m from_div_45g45gg"}).text,
                    "subject": email.find("div", {"class": "e7m subj_div_45g45gg"}).text,
                    "time": email.find("div", {"class": "e7m time_div_45g45gg"}).text,
                }
                emails.append(data)
        
            return emails
        
    def wait_for_new_email(self, delay: None=None, timeout: int=60) -> dict:
        """
        Waits for a new mail (using websockets), returns the data of the incoming email, None if timeout is hit or an error occurs\n
        Args:\n
        timeout - the time which is allowed to pass before forcefully stopping, <=0 -> no timeout. Note that it does not stop at exactly the time due to being sync
        delay - not used, simply for compatability
        """

        if timeout > 0: 
            start = time()

        def on_message(ws: websocket.WebSocketApp, message: str):
            nonlocal manual_stop
            
            if message.startswith("0"):
                ws.send("40")
                
            elif message.startswith("40"):
                ws.send(f'42["watch_for_my_email","{self.email}"]')
        
            elif message.startswith("42"):
                data = json.loads(message[2:])

                if data[0] == "new_email":
                    manual_stop = True
                    ws.close()
                    
                    data = json.loads(data[1])
                    soup = BeautifulSoup(data["tddata"], "lxml")
                    
                    nonlocal email_data
                    email_data = {
                        "id": data["clickgo"].rsplit("/", maxsplit=1)[1],
                        "from": soup.find("div", {"class": "from_div_45g45gg"}),
                        "subject": soup.find("div", {"class": "subj_div_45g45gg"}),
                        "time": soup.find("div", {"class": "time_div_45g45gg"})
                    }
            
            elif message.startswith("2"): # ping
                ws.send("3")
            
            if timeout > 0 and time()-start >= timeout:
                manual_stop = True
                ws.close()

        def on_close(ws, *args):
            
            if not manual_stop:
                if timeout > 0 and time()-start >= timeout:
                    return None
                
                ws.close()
                ws = websocket.WebSocketApp("wss://generator.email/socket.io/?EIO=4&transport=websocket", on_message=on_message, on_close=on_close)
                ws.run_forever()

        email_data = None
        manual_stop = False
        ws = websocket.WebSocketApp("wss://generator.email/socket.io/?EIO=4&transport=websocket", on_message=on_message, on_close=on_close)
        ws.run_forever()
        return email_data
