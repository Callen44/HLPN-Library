# Data Transfers
Of course, the entire point of using a protocol like HTP is to eventually be able to send some kind of data. Systems that implement HTP need to be able to connect more than they need to be able to send data, at lease, as far as the protocol is concerned.

## Data in transfer
In order to be easy to layer on as many other protocols as possible, HTP can only send and recieve strings. For basic connecting, pinging, and other protocol maintinence this is fine, and for many other things this may still be fine. But often, you don't only want to send text, you may want to send images, raw data, or other things. 

to resolve ths issue, HTP converts all non-maintinence data to hexadecimal before sending.