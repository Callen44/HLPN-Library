# this file contains the connector classes, and runs the HTP library, note that this is IRREGULAR, do not actually do this in production.
# this script tests the htp program
import worker
import time

# line variables store the communication, basically a simulated radio connection
line = str()
lasttotransmit = None # we don't want a station to recieve it's own transmission.

class Connector():
    def __init__(self):
        pass
    def transmit(self, msg, tocall, fromcall): # transmit revieves fromcall and tocall, in case they are needed by the lower level protocol
        global line
        # clean out the line before transmitting, that way the stations don't need 2 lines
        line = None
        line = msg
        lasttotransmit = self
    def recieve(self):
        global line
        if lasttotransmit != self: # this prevents a station from revieving it's own message
            # We don't want the same station to recieve the same message multiple times, so we clear out the line variable after recieving
            localline = line
            line = None
            return localline
        else:
            pass
    
def basictest():
    connector1 = Connector()
    connector2 = Connector()

    # the workers have the call signs, test1 and 2
    worker1 = worker.HTPWorker('TEST1', 'TEST2', connector1, pingdelay=3)
    worker2 = worker.HTPWorker('TEST2', 'TEST1', connector2, pingdelay=3)

    worker1.initiate_connection()
    # stop the test after a set amount of time
    timepertest = 10
    timestart = time.time()
    while (time.time() - timestart) < float(timepertest):
        worker2.update()
        worker1.update()

    worker1.endcall()
    worker2.update()

# if this file is run directly, then begin a full test
if __name__ == "__main__":
    basictest()