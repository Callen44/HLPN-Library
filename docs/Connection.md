# Connections
This file contains data on the type of data involved in making, using and maintaing connections between devices. A few important things to note are:

1. Just in case you forgot, HTP is not a stand alone protocol and requires a lower level protocol.
2. All connections are case insenseitive, ASCII should be used in all structured protocols, or any protocol that does not provide its own text system.
3. The station that transmits always says its call sign first, then a space, and the recieving call sign. Both call signs must be provided and in this order.
4. Below you will see something like `[Transmitting station's call sign]`, this is to be replaced in real usage by the call sign, do not include brackets *ever*.
5. Call signs must be included, even if a wrapping protocol like AX.25 also provides this information. this is because HTP is supposed to operate in as many situations as possible.
6. Only 2 stations may take part in a HTP connection.

# Open Connection
HTP, using the lower level protocol initiates the connection and operates it as described below.
1. 

### Request to Open the Connection
CON stands for CONnection, because it opens the connection. Taking up a station's request for opening a connection is optional, as described later.

```
CON [Transmitting station's call sign] [Recieving station's call sign]
```

### Accepting or Rejecting 
CAC stands for Connection ACcepted, a station that recieves a CON responds with either CAC or CRE.

```
CAC [Transmitting station's call sign] [Recieving station's call sign]
```

CRE stands for Connection REjected

```
CRE [Transmitting station's call sign] [Recieving station's call sign]
```

Remember: CRE immediately ends the connection and no transmitting to a station the rejects a connection should be made!

### Finalizing the Connection-Making process
CMA stands for Connection MAde, after a connection has been accepted with CAC the other station confirms that it heard the accepting signal with CMA.

```
CMA [Transmitting station's call sign] [Recieving station's call sign]
```

# Maintaining the Connection
the 2 stations are now connected, but we need to maintain the connection, otherwise the station's connection may be faulty without the operator's knowledge, due to changing conditions, or other factors that may harm the signal without the operator or computer's knowledge.

## Pinging
Pinging is not optional and connected stations must respond to ping requests or the other station my be confused and end the connection. To prevent packet collision the station who sent the initial CON request is responsible for managing pinging, and must ping at least every minute

To ensure that both stations are able to take full advantage of the ping system, the signal is bounced twice. The first station sends the initial ping, then the seccond station sends a pong, the first station then ends the ping with a third message.

Pinging is done like so:
```
PNG [Transmitting station's call sign] [Recieving station's call sign]
```

The seccond station then pongs like this:

```
POG [Transmitting station's call sign] [Recieving station's call sign]
```

And the ping is ended with a
```
EPG [Transmitting station's call sign] [Recieving station's call sign]
```