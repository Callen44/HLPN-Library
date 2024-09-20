# Data Transfers
Of course, the entire point of using a protocol like HTP is to eventually be able to send some kind of data. Systems that implement HTP need to be able to connect more than they need to be able to send data, at lease, as far as the protocol is concerned.

## Data in transfer
In order to be easy to layer on as many other protocols as possible, HTP can only send and recieve strings. For basic connecting, pinging, and other protocol maintinence this is fine, and for many other things this may still be fine. But often, you don't only want to send text, you may want to send images, raw data, or other things. 

to resolve ths issue, HTP converts all non-maintinence data streams to hexadecimal before sending.

HTP does not provide anything like HTTP out of the box (don't let the similar name fool you). HTP does not fit into the application level of the ISO model, rather it is intended to be either a transport layer or a data link layer protocol.

# Short Data Streams
Short data streams are a basic way of transferring data, they look like this
```
SDS [Transmitting station's call sign] [Recieving station's call sign] [Data in hexadecimal] [Number of digits in origional signal]
```
To prevent any errors in the data, the number of digits in the hexadecimal message is also sent with the data, to provide basic error correction. Short data streams are short and don't support: advanced error correction or fragmentation/splitting data packets up.

# Long Data Streams
Long data streams are what are the most useful though, they are made up of several packets that are assembled into a larger piece of data.
Each piece of a long data stream is sent as a seperate packet, there can be pings and other maintinence data sent in between the long data stream packets.
Because it would be very difficult to implement, it is not reccommended for there to be 2 Long Data streams at once, though you may write software with this feature.
A long data stream must be declared and the stream given an ID, that way it can be determined what packets go with the stream.
Each packet of a long data stream, must bear the ID for its stream, and also have a tag for the order, so that they can be reassembled.
The ID does not need to have anything special about it, it just needs to be uniquie, and an intiger.

## Declaring a Long Data Stream
Long data streams are declared like so, (BLD stands for Begin Long Data stream)
After all of the hexadecimal fragments have been added together, the total number of digits must be equal to the last part of the BLD
```
BLD [Transmitting station's call sign] [Recieving station's call sign] [ID to be assigned] [The total number of packets to be transmitted]
```

## Transferring packets as in the stream
Each packet in the stream needs it's own unique identifier, these identifiers must be assigned incrimentally starting with 0 according to the packet order
Transferring data in these streams is done like so, (LDP stands for Long Data stream Part)
```
LDP [Transmitting station's call sign] [Recieving station's call sign] [Stream's ID] [Data in hexadecimal] [the Packet's Unique identifier]
```

## ending the stream
All good things must come to an end, and the reciever must know that it has all of the packets eventually.
To end a stream the device that is doing the transmitting must transmit LDE (Long Data End)
```
LDE [Transmitting stations's call sign] [Recieving station's call sign] [Stream's ID]
```