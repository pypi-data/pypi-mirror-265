import json

from bs4 import BeautifulSoup
import requests

from ._constructors import _Livewire

class Tempdashmail_gg(_Livewire):
    """An API Wrapper around the https://temp-mail.gg/ website"""

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
                "first_data": "{ in_app: false, qr_code: false, show_loader: true, load_qr: false }",
                "second_data": ("div", "{ show: false, id: 0 }")
            },
            urls={
                "base": "https://temp-mail.gg/mailbox",
                "app": "https://temp-mail.gg/livewire/message/frontend.app",
                "actions": "https://temp-mail.gg/livewire/message/frontend.actions"
            },
            order=0, name=name, domain=domain, exclude=exclude
        )

    @staticmethod
    def get_valid_domains() -> list[str] | None:
        """
            Returns a list of a valid domains, None if failure
        """
        r = requests.get("https://temp-mail.gg/mailbox")
       
        if r.ok:
            soup = BeautifulSoup(r.text, "lxml")
            data = json.loads(soup.find("div", {"x-data": "{ in_app: false, qr_code: false, show_loader: true, load_qr: false }"})["wire:initial-data"])

            return data["serverMemo"]["data"]["domains"]
                                        