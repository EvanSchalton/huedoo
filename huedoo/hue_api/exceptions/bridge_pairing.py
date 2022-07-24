class BridgePairingException(Exception):
    """
    Error occured when pairing with the bridge
    """

    def __init__(self, msg: str):
        super().__init__(f"BridgePairingException: {msg}")


class BridgeButtonNotPushed(BridgePairingException):
    """
    Bridge Pairing failed because bridge button not pressed
    """

    def __init__(self):
        super().__init__("Bridge Button Not Pressed")


class UnknownAppName(BridgePairingException):
    """
    Bridge Pairing failed because an unknown username was provided
    """

    def __init__(self, username: str):
        super().__init__(f"UnknownAppName: '{username}'")
