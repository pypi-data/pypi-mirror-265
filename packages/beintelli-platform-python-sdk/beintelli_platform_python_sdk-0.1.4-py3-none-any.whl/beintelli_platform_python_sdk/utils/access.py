"""Containing class access"""

class Access:
    """Wrapper for the access-token"""
    def __init__(self):
        self.access_token =""

    def set_access_token(self, access_token:str)->None:
        """Simple setter

        Args:
            access_token (str)
        """
        self.access_token = access_token

    def get_access_token(self)->str:
        """Simple Getter

        Returns:
            str: access token
        """
        return self.access_token
