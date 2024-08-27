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