# this file contains the connector classes, and runs the HTP library, note that this is IRREGULAR, do not actually do this in production.
# this script tests the htp program
import worker
import time
from testerconnector import Connector

# line variables store the communication, basically a simulated radio connection
line = str()
lasttotransmit = None # we don't want a station to recieve it's own transmission.
    
def basictest(): # test connecting, pinging, and disconnecting
    connector1 = Connector()
    connector2 = Connector()

    # the workers have the call signs, test1 and 2
    worker1 = worker.HTPWorker('TEST1', 'TEST2', connector1, pingdelay=3)
    worker2 = worker.HTPWorker('TEST2', 'TEST1', connector2, pingdelay=3)

    worker1.initiate_connection()
    # stop the test after a set amount of time
    timestart = time.time()
    while (time.time() - timestart) < float(10):
        worker2.update()
        worker1.update()

    worker1.endcall()
    worker2.update()

def datatest(): # test connecting and sending data.
    connector1 = Connector()
    connector2 = Connector()

    # the workers have the call signs, test1 and 2
    worker1 = worker.HTPWorker('TEST1', 'TEST2', connector1, pingdelay=3)
    worker2 = worker.HTPWorker('TEST2', 'TEST1', connector2, pingdelay=3)

    worker1.initiate_connection()
    # run the test for a set amount of time before transmitting data
    timestart = time.time()
    while (time.time() - timestart) < float(5):
        worker2.update()
        worker1.update()
    
    worker1.transmitshortdata('10101010101010101010')

    # begin running again
    timestart = time.time()
    while(time.time() - timestart) < float(3):
        worker2.update()
        worker1.update()

    worker1.endcall()
    worker2.update()

def longdatatest():
    connector1 = Connector()
    connector2 = Connector()

    # the workers have the call signs, test1 and 2
    worker1 = worker.HTPWorker('TEST1', 'TEST2', connector1, pingdelay=3)
    worker2 = worker.HTPWorker('TEST2', 'TEST1', connector2, pingdelay=3)

    worker1.initiate_connection()
    # run the test for a set amount of time before transmitting data
    timestart = time.time()
    while (time.time() - timestart) < float(5):
        worker2.update()
        worker1.update()
    
    worker2.transmitlongdata('101010101010101010100000000000001111111111')

    # begin running again
    timestart = time.time()
    while(time.time() - timestart) < float(3):
        worker1.update()
        worker2.update()

    worker1.endcall()
    worker2.update()

# if this file is run directly, then begin a full test
if __name__ == "__main__":
    basictest()
    print("\n\nBasic Test Done!")
    datatest()
    print("\n\nData Test Done!")
    longdatatest()