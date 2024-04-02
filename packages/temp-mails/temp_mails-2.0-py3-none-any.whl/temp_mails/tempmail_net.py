from ._constructors import _Tempail_Tempmailnet

class Tempmail_net(_Tempail_Tempmailnet):
    """An API Wrapper around the https://tempmail.net/ website"""

    def __init__(self):
        super().__init__(base_url="https://tempmail.net", offset_of_email_content=1)
