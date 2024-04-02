from ._constructors import _Minuteinbox_Disposablemail_Fakemail

class Minuteinbox_com(_Minuteinbox_Disposablemail_Fakemail):
    """An API Wrapper around the https://www.minuteinbox.com/ website"""

    def __init__(self):
        super().__init__(base_url="https://www.minuteinbox.com")
