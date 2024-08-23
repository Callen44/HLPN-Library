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
        self.connector.transmit("CON {} {}".format(self.mycall.upper(), self.yourcall.upper()))
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
                print("I'm {} Connecting to {}".format(self.mycall, args[1]))
                self.tryingtoconnect = True
                self.connector.transmit("")