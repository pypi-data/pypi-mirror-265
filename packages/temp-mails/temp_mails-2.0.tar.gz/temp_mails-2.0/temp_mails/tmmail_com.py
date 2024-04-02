from bs4 import BeautifulSoup
import requests

from ._constructors import _WaitForMail, _generate_user_data

class Tmmail_com(_WaitForMail):
    """An API Wrapper around the https://tm-mail.com/ website"""

    def __init__(self, name: str=None, domain: str=None, exclude: list[str]=None):
        """
        Generate an inbox\n
        Args:\n
        name - name for the email, if None a random one is chosen\n
        domain - the domain to use, domain is prioritized over exclude\n
        exclude - a list of domain to exclude from the random selection\n
        """
        super().__init__(0)

        self._session = requests.Session()

        r = self._session.get("https://tm-mail.com")
        if not r.ok:
            raise Exception(f"Something went wrong on Email Creation, status: {r.status_code}")
        
        self._token = BeautifulSoup(r.text, "lxml").find("meta", {"name": "csrf-token"})["content"]

        r = self._session.post("https://tm-mail.com/messages", data={"_token": self._token})
        if not r.ok:
            raise Exception(f"Something went wrong on Email Creation, status: {r.status_code}")
        

        if not domain and not name and not exclude:
            self.email = r.json()["mailbox"]
            self.name, self.domain = self.email.split("@", maxsplit=1)
            return

        self.name, self.domain, self.email, self.valid_domains = _generate_user_data(name, domain, exclude, self.get_valid_domains())

        data = {
            "name": self.name,
            "domain": self.domain,
            "token": self._token
        }

        r = self._session.post("https://tm-mail.com/create", data=data)
        if not r.ok:
            raise Exception(f"Something went wrong on Email Creation, status: {r.status_code}, response content:\n{r.text}")
        
    @staticmethod
    def get_valid_domains() -> list[str]:
        """
        Returns a list of valid domains of the service (format: abc.xyz) as a list
        """

        r = requests.get("https://tm-mail.com/change")
        if r.ok:
            soup = BeautifulSoup(r.text, "lxml")
            email_options = soup.find_all("option")
            
            return [option["value"] for option in email_options]


    def get_inbox(self) -> list[dict]:
        """
        Returns the inbox including the content.
        """
        
        r = self._session.post("https://tm-mail.com/messages", data={"_token": self._token})
        if r.ok:
            return r.json()["messages"]
        