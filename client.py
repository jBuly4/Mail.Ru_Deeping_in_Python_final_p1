import socket
import time

class ClientError(Exception):

    def __init__(self, text):
        self.text = text

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




    def put(self, key, value, timestamp=None):
        normal_answ = 'ok\n\n'
        try:
            if timestamp == None:
                self.connection.send(key, value, int(time.time()))
            else:
                self.connection.send(key, value, int(timestamp))
            data_recvd = self.connection.recv(1024)
            if data_recvd != normal_answ:
                raise ClientError("ClientError")
        except ClientError as clErr:
            print(clErr) # dunno if it would work
            # raise ClientError

    def __del__(self):
        self.connection.close()
