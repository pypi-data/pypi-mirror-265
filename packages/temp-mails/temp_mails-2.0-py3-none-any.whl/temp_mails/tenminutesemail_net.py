from bs4 import BeautifulSoup
import requests

from ._constructors import _Tenminutesemail_Eztempmail_Tmailgg

class Tenminutesemail_net(_Tenminutesemail_Eztempmail_Tmailgg):
    """An API Wrapper around the https://10minutesemail.net/ website"""

    def __init__(self, name: str=None, domain: str=None, exclude: list[str]=None):
        """
            Generate an inbox\n
            Args:\n
            name - name for the email, if None a random one is chosen\n
            domain - the domain to use, domain is prioritized over exclude\n
            exclude - a list of domain to exclude from the random selection\n
        """
        super().__init__(base_url="https://10minutesemail.net", name=name, domain=domain, exclude=exclude)

    
    @staticmethod
    def get_valid_domains() -> list[str]:
        """
        Returns a list of valid domains of the service (format: abc.xyz) as a list
        """

        r = requests.get("https://10minutesemail.net/change")
        if r.ok:
            if "Bot Verification" in r.text:
                raise Exception("Error, you need to verify Captcha manually on https://10minutesemail.net.") 
            soup = BeautifulSoup(r.text, "lxml")
            return [domain.text for domain in soup.find("select", {"name": "domain"}).findChildren("option")]
        