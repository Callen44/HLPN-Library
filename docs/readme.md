# HTP (Ham Transport Protocol)
Ham transport protocol is a wrappable protocol that is designed to enable the exact same ham radio data and apps to be used, while the radio, modulation type, and other specifics of the connection can still vary greatly. HTP is designed to be lightweight and fast, but only supports 2 stations in a connection at a time.

# What does it do?
HTP is basically TCP for ham radio, it only sends the data needed to:
1. open and close connections
2. maintain connections
3. check speed
4. send data at the maximum speed that is posible & reasonable for both station's hardware