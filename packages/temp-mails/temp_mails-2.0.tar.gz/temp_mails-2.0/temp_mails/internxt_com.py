import requests
from ._constructors import _WaitForMail

class Internxt_com(_WaitForMail):
    """An API Wrapper around the https://internxt.com/temporary-email website"""

    def __init__(self):
        """
            Generate a random inbox\n
        """
        super().__init__(0)

        self._session = requests.Session()
        
        r = self._session.get("https://internxt.com/api/temp-mail/create-email")
        if not r.ok:
            raise Exception("Error on creation", r, r.text)
        
        data = r.json()
        self._token = data["token"]
        self.email = data["address"]
        self.name, self.domain = self.email.split("@", maxsplit=1)

    def get_inbox(self) -> list[dict]:
        """
        Returns the inbox of the email as a list with mails as dicts list[dict, dict, ...]
        """

        r = self._session.get("https://internxt.com/api/temp-mail/get-inbox?token="+self._token)
        
        if r.ok:
            return r.json()["emails"]
