from ._constructors import _Tenminemail_Tempailorg

class Tenminemail_com(_Tenminemail_Tempailorg):
    """An API Wrapper around the https://10minemail.com/ website"""

    def __init__(self):
        """
        Generate a random inbox
        """
        super().__init__(urls={
            "mailbox": "https://web2.10minemail.com/mailbox/",
            "messages": "https://web2.10minemail.com/messages/"
        })
        