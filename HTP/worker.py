class HTPWorker():
    def __init__(self, mycall, yourcall, connector, accepting=True):
        # Load the main paramaters into variables
        self.mycall = str(mycall)
        self.yourcall = str(yourcall)
        self.connector = connector
        self.accepting = accepting # Remembers if the program is accepting new connections
        self.maxconnections = 1 # I hope to add support for multiple connections later

        # initilize variables to be used later
        self.connected = False
        self.tryingtoconnect = False
    def initiate_connection(self):
        self.tryingtoconnect = True
        self.connector.transmit("CON {} {}".format(self.mycall.upper(), self.yourcall.upper()))
    def ping(self):
        # this function is responsible for managing all pinging that goes on
        pass
    def update(self):
        # this function recieves data and then processes it
        data = self.connector.recieve()
        if data == None: # if nothing was recieved, then there is no sense in keeping this function running any longer
            return
        
        data = str(data)
        print("Recieved data: {}".format(data))

        # begin evaluating what the data is and what needs to be done
        args = data.split()
        prefix = data[:3] # the prefix is the first 3 characters of the data and tells us what we are dealing with

        if prefix == "CON": # the other stations wants to start a connection
            # check if this is allowed, and if we are the station he is trying to connect
            if not self.connected and self.accepting and not self.tryingtoconnect and args[2] == self.mycall:
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
            print("I'm {}, I've just revieved CMA for a connection with {}\n\nCommencing {}'s Pinging".format(self.mycall, self.yourcall, self.mycall))

            self.ping() # begin the pinging process