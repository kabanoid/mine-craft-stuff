from mcrcon import MCRcon

class Connection:
    def __init__(self, address, port, secret):
        self.mcr = MCRcon(address, secret)
        self.mcr.connect()

    def send(self, msg):
        resp = self.mcr.command(msg)
        return resp
