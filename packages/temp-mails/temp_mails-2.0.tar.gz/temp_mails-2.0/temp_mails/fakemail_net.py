from ._constructors import _Minuteinbox_Disposablemail_Fakemail

class Fakemail_net(_Minuteinbox_Disposablemail_Fakemail):
    """An API Wrapper around the https://www.fakemail.net/ website"""
    
    def __init__(self):
        super().__init__(base_url="https://www.fakemail.net")
