import json

from bs4 import BeautifulSoup
import requests

from ._constructors import _Livewire2

class Mostakbile_com(_Livewire2):
    """An API Wrapper around the https://mostakbile.com website"""

    def __init__(self, name: str=None, domain: str=None, exclude: list[str]=None):
        """
            Generate an inbox\n
            Args:\n
            name - name for the email, if None a random one is chosen\n
            domain - the domain to use, domain is prioritized over exclude\n
            exclude - a list of domain to exclude from the random selection\n
        """
        
        super().__init__(
            strings={
                "first_data": "{ in_app: true }",
                "first_data2": "{ in_app: false }",
                "second_data": "{ show: false, id: 0 }"
            },
            urls={
                "base": "https://mostakbile.com",
                "mailbox": "https://mostakbile.com/mailbox",
                "app": "https://mostakbile.com/livewire/message/frontend.app",
                "actions": "https://mostakbile.com/livewire/message/frontend.actions"
            },
            order=0, name=name, domain=domain, exclude=exclude
            )


    @staticmethod
    def get_valid_domains() -> list[str] | None:
        """
            Returns a list of a valid domains, None if failure
        """
        r = requests.get("https://mostakbile.com/")
       
        if r.ok:
            soup = BeautifulSoup(r.text, "lxml")
            data = json.loads(soup.find("div", {"x-data": "{ in_app: true }"})["wire:initial-data"])

            return data["serverMemo"]["data"]["domains"]
