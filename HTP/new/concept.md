# Decompose the problem
1. We need a Connector that provide TNC support
2. We need a core device that recieves all data and determines which handler we need to send it to
3. We need a handler for each type of packet.
    1. the handlers need the ability to keep their memory across usage, so that they are able to respond to messages split across multiple packets.

# Ideas
- Each transport connection has a seperate process that is responsible for it.