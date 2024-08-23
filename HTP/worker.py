import time # used for measuring ping speed

class HTPWorker():
    def __init__(self, mycall, yourcall, connector, accepting=True):
        # Load the main paramaters into variables
        self.mycall = str(mycall)
        self.yourcall = yourcall # this can be left blank, if so the station will pair with any other stations that want to pair with it
        self.connector = connector
        self.accepting = accepting # Remembers if the program is accepting new connections
        self.maxconnections = 1 # I hope to add support for multiple connections later

        # initilize variables to be used later
        self.connected = False
        self.tryingtoconnect = False
        self.pingingnow = False
        self.pingspeednow = int()
        self.pingspeeds = list()
        self.livepingtime = None # this stores the time that is used in calculating the ping speed
        self.lastping = int() # this stores the last time that a ping was successfully made, prevents from having too many pings.
    def initiate_connection(self):
        self.tryingtoconnect = True
        self.connector.transmit("CON {} {}".format(self.mycall.upper(), self.yourcall.upper()))
    def ping(self):
        # this function is responsible for starting pinging, but not responding to a ping
        self.connector.transmit("PNG {} {}".format(self.mycall, self.yourcall))
        self.pingingnow = True
        self.livepingtime = time.time()
    def update(self):
        # this function recieves data and then processes it
        data = self.connector.recieve()
        
        # this part of the function runs scheduled tasks
        if time.time() - self.lastping == 30.0:
            self.ping()


        if data == None: # if nothing was recieved, then there is no sense in keeping this function running any longer
            return

        # this part of the function parses packets and responds to them
        data = str(data).upper()
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
                    self.connector.transmit("CAC {} {}".format(self.mycall, self.yourcall))

            if prefix == "CAC" and self.tryingtoconnect and args[2] == self.mycall:
                # the other station just accepted my request
                print("I'm {} Confirming a connection with {}".format(self.mycall, self.yourcall))

                # we have now connected, so we should stop accepting other connections, and make note of the other changes
                self.tryingtoconnect = False
                self.connected = True
                self.accepting = False

                self.connector.transmit("CMA {} {}".format(self.mycall, self.yourcall))
            if prefix == "CMA" and self.tryingtoconnect:
                # we have now connected, so we should stop accepting other connections, and make note of the other changes
                self.tryingtoconnect = False
                self.connected = True
                self.accepting = False
                print("I'm {}, I've just revieved CMA for a connection with {}\n\nCommencing my ({}'s) Pinging".format(self.mycall, self.yourcall, self.mycall))

                self.ping() # begin the pinging process
            if prefix == "PNG" and self.connected:
                print("I'm {} recieving a ping, and responding".format(self.mycall))
                self.connector.transmit("POG {} {}".format(self.mycall, self.yourcall))
                self.pingingnow = True
                self.livepingtime = time.time()
            if prefix == "POG" and self.connected:
                print("I'm {} recieving a POG, responding by ending the ping".format(self.mycall))
                self.connector.transmit("EPG {} {}".format(self.mycall, self.yourcall))
                self.pingingnow == False
                now = time.time()
                self.pingspeednow = now - self.livepingtime
                self.livepingtime = None
                self.lastping = now
                self.pingspeeds.append(self.pingspeednow)
                print("Ping Speed: {}".format(self.pingspeednow))