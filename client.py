import socket

class Client:

    """client for putting and getting metrics """

     def __init__(self, adr, port, timeout=None):
         self.adr = adr
         self.port = port
         self.timeout = timeout

         self.connection = socket.socket()
         self.connection.connect((self.adr, seld.port), timeout)

         # with socket.socket() as connection:
         #     connection.connect((self.adr, seld.port), timeout)

    # def get(self, key):
    #     data_returned = {}
    #     self.connection.send(key)
    #     try:
    #         data_returned = self.connection.recv()
    #     except ClientError as e:
    #         raise




    # def put(self, key, value):
    #

    def __del__(self):
        self.connection.close()
