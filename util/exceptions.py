class Error(Exception):
    """  Base Class for exceptions in this module.  """
    pass


class APIKeyError(Error):
    """
    Exception raised when there is an issue with the APIKey

    Attributes:
        APIKey -- The APIKey in the API-Key File
        message -- Message to be displayed to the user
    """
    def __init__(self, APIKey, message):
        self.APIKey = APIKey
        self.message = message
