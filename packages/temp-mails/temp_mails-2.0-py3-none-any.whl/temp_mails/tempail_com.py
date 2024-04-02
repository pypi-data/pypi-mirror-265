from ._constructors import _Tempail_Tempmailnet

class Tempail_com(_Tempail_Tempmailnet):
    """An API Wrapper around the https://tempail.com website"""

    def __init__(self):
        super().__init__(base_url="https://tempail.com", offset_of_email_content=0)
                                                