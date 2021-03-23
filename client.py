import socket

class Client:

    """client for putting and getting metrics """

     def __init__(self, adr, port, timeout=5):
         self.adr = adr
         self.port = port
         self.timeout = timeout

         with socket.socket() as connection:
             connection.connect((self.adr, seld.port), timeout)
             
