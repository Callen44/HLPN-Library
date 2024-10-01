class Connector():
    def __init__(self):
        pass
    def transmit(self, msg, tocall, fromcall): # transmit revieves fromcall and tocall, in case they are needed by the lower level protocol
        global line, lasttotransmit
        # clean out the line before transmitting, that way the stations don't need 2 lines
        line = None
        line = msg
        lasttotransmit = self
    def recieve(self):
        global line, lasttotransmit
        if lasttotransmit != self: # this prevents a station from revieving it's own message
            # We don't want the same station to recieve the same message multiple times, so we clear out the line variable after recieving
            localline = line
            line = None
            return localline
        else:
            pass
    def update(self):
        pass