import time # used for measuring ping speed

# set constants
GOOD_ARGS = {
    'CON',
    'PNG',
    'ETM',
    'RTM',
    'CAC',
    'CMA',
    'POG',
    'EPG',
    'CRE',
    'ETM',
    'RTM',
    'SDS',
}

class HTPWorker():
    def __init__(self, mycall, yourcall, connector, accepting=True, pingdelay=30, timeout=60):
        # Load the main paramaters into variables
        self.mycall = str(mycall)
        self.yourcall = yourcall # this can be left blank, if so the station will pair with any other stations that want to pair with it
        self.connector = connector
        self.accepting = accepting # Remembers if the program is accepting new connections
        self.maxconnections = 1 # I hope to add support for multiple connections later
        self.pingdelay = float(pingdelay)
        self.timeout = timeout # used for timeouts

        # initilize variables to be used later
        self.connected = False
        self.tryingtoconnect = False
        self.pingingnow = False
        self.pingspeednow = int()
        self.pingspeeds = list()
        self.rtmtries = int() # used for remembering the number of times that a message was retransmitted, useful when timeouting
        self.livepingtime = None # this stores the time that is used in calculating the ping speed
        self.lastping = int() # this stores the last time that a ping was successfully made, prevents from having too many pings.
        self.lastmsg = str() # this records the last message that was sent, this way if it needs to be resent there is an easy way to do so.
        self.pinger = str() # this remembers who is supposed to ping, if It's not me then don't ping regularly
        self.recieved = str() # stores the last received message for a while, this decreases stress on the TNC
    def initiate_connection(self):
        self.tryingtoconnect = True
        self.organizedtransmit("CON {} {}".format(self.mycall.upper(), self.yourcall.upper()))
    def ping(self):
        if self.pingingnow:
            return # we don't want to run the function if a ping is already in progress

        # this function is responsible for starting pinging, but not responding to a ping
        self.organizedtransmit("PNG {} {}".format(self.mycall, self.yourcall))
        self.pingingnow = True
        self.livepingtime = time.time()
    def organizedtransmit(self, msg):
        # this is a checkpoint for all transmissions to ensure that they are recorded and treated properly, it records messages so they can be resent
        self.lastmsg = msg
        print("Transmitting: {}".format(msg))
        self.connector.transmit(msg.upper(), fromcall=self.mycall.upper(), tocall=self.yourcall.upper())
    def organizedrecieve(self): # unlike organized transmit, this message is not ment to be called periodically, it is only used once each update
        self.recieved = self.connector.recieve()
    def endcall(self):
        self.organizedtransmit("ETM {} {}".format(self.mycall, self.yourcall))
    def update(self): # to keep the code organized the maintain connection system and the data processing systems are split up.
        self.organizedrecieve()
        try:
            self.check_data()
        except SyntaxError:
            if self.rtmtries < self.timeout and self.connected: # ensure the function will timeout, and that it will not continue if we aren't connected to the station
                print("Data was illegable, requesting retransmit")
                self.request_retransmit()
            return
        # if everything went well with recieving, move on
        self.maintain_con()
    def check_data(self): # this only runs a basic check, not a more advanced check with checksum
        data = self.recieved
        if data == None:
            return
        prefix = self.recieved[:3]
        args = list(data)
        if prefix in GOOD_ARGS: # check for legible prefix
            pass
        else:
            raise SyntaxError("Recieved data is illegable") # !!!!!!!!!!! this needs to be replaced with a better error
        if len(args[2]) < 6 and len(args[2]) > 4 and args[2] == self.yourcall: # good call sign
            return True
    def request_retransmit(self):
        self.organizedtransmit("RTM {} {}".format(self.mycall.upper(), self.yourcall.upper()))
    def maintain_con(self):
        # this function recieves data and then processes it
        data = self.recieved

        # this part of the function runs scheduled tasks
        if time.time() - self.lastping >= float(self.pingdelay) and self.lastping > 0 and self.pinger == self.mycall: # when this function is run the first few times it is almost inevitable that lastping will be low
            self.ping()

        if data == None: # if nothing was recieved, then there is no sense in keeping this function running any longer
            return

        # this part of the function parses packets and responds to them
        data = str(data).upper() # reformat data
        print("\nRecieved data: {}".format(data))

        # begin evaluating what the data is and what needs to be done
        args = data.split()
        prefix = data[:3] # the prefix is the first 3 characters of the data and tells us what we are dealing with
        if args[2] == self.mycall: # this checks if the packet was sent to our station, otherwise it should be ignored
            if prefix == "CON": # the other stations wants to start a connection
                # check if this is allowed, and if we are the station he is trying to connect
                if not self.connected and self.accepting and not self.tryingtoconnect:
                    # let's connect!
                    print("I'm {} Accepting a connection to {}".format(self.mycall, args[1]))
                    self.tryingtoconnect = True
                    self.organizedtransmit("CAC {} {}".format(self.mycall, self.yourcall))
                else:
                    print("I'm {}, and am rejecting a connection with {}".format(self.mycall, self.yourcall))
                    self.organizedtransmit("CRE {} {}".format(self.mycall, self.yourcall))

            if prefix == "CAC" and self.tryingtoconnect and args[2] == self.mycall:
                # the other station just accepted my request
                print("I'm {} Confirming a connection with {}".format(self.mycall, self.yourcall))

                # we have now connected, so we should stop accepting other connections, and make note of the other changes
                self.tryingtoconnect = False
                self.connected = True
                self.accepting = False

                self.organizedtransmit("CMA {} {}".format(self.mycall, self.yourcall))
            if prefix == "CMA" and self.tryingtoconnect:
                # we have now connected, so we should stop accepting other connections, and make note of the other changes
                self.tryingtoconnect = False
                self.connected = True
                self.accepting = False
                print("I'm {}, I've just revieved CMA for a connection with {}\n\nCommencing my ({}'s) Pinging".format(self.mycall, self.yourcall, self.mycall))

                self.pinger = self.mycall # this stores who is supposed to ping
                self.ping() # begin the pinging process
            if prefix == "PNG" and self.connected:
                print("I'm {} recieving a ping, and responding".format(self.mycall))
                self.organizedtransmit("POG {} {}".format(self.mycall, self.yourcall))
                self.pingingnow = True
                self.livepingtime = time.time()
            if prefix == "POG" and self.connected:
                print("I'm {} recieving a POG, responding by ending the ping".format(self.mycall))
                self.organizedtransmit("EPG {} {}".format(self.mycall, self.yourcall))
                self.pingingnow = False
                now = time.time()
                try:
                    self.pingspeednow = now - self.livepingtime
                except:
                    print("NOT FATAL ERROR! ping speed could not be calculated")
                self.livepingtime = None
                self.lastping = now
                self.pingspeeds.append(self.pingspeednow)
                print("Ping Speed: {}".format(self.pingspeednow))
            if prefix == "EPG" and self.connected:
                self.pingingnow = False
                now = time.time()
                self.pingspeednow = now - self.livepingtime
                self.livepingtime = None
                self.lastping = now
                self.pingspeeds.append(self.pingspeednow)
                print("Ping Speed: {}".format(self.pingspeednow))
            if prefix == "CRE" and self.tryingtoconnect and self.connected == False: # this checks if the rejection signal was returned while connection and responds
                self.tryingtoconnect = False
                raise ConnectionRefusedError("The other station's system refused the connection, this is a fatal error and we cannot continue.")
            if prefix == "ETM":
                print("I'm {}, The transmission has been ended".format(self.mycall))
                self.connected = False
            if prefix == "RTM": #!!!!!!!!ATTENTION!!!!!!!!!! I need better implementing
                print("I'm {} retransmitting upon request".format(self.mycall))
                self.organizedtransmit(self.lastmsg)
            if prefix == "SDS": #this function cannot process data, so send it off for processing
                self.processdata()
    def processdata(self):
        fulldata = self.recieved
        fulldatalist = fulldata.split()
        print("incoming data!")
        recieveddata = fulldatalist[3]
        print(fulldatalist[4])
        if len(recieveddata) == int(fulldatalist[4]): # check if the data is as long as it is supposed to be, this is very important for data error correction
            pass
        else:
            print("Bad data recieved, requesting retransmit")
            self.request_retransmit()
            return
        # Extract the origional data and call a handler'
        origionaldata = bin(int(recieveddata, base=16))[2:].zfill(int(fulldatalist[4]))# convert to binary, using the number of digits in the error correction data
        print(origionaldata)
    def transmitdata(self,data):
        hexdata = hex(int(data, base=2))
        datalength = len(hexdata)
        self.organizedtransmit("SDS {} {} {} {}".format(self.mycall, self.yourcall, hexdata, datalength))