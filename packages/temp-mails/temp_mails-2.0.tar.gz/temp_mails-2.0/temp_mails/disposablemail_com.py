from ._constructors import _Minuteinbox_Disposablemail_Fakemail

class Disposablemail_com(_Minuteinbox_Disposablemail_Fakemail):
    """An API Wrapper around the https://www.disposablemail.com/ website"""
    def __init__(self):
        super().__init__(base_url="https://www.disposablemail.com")
