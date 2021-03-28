import socket
import time

class ClientError(Exception):

    # def __init__(self, text="ClientError"):
    #     self.text = text
    pass

class Client:


    """client for putting and getting metrics """

    def __init__(self, adr, port, timeout=None):
        self.adr = adr
        self.port = port
        self.timeout = timeout
        try:
            self.connection = socket.create_connection((self.adr, self.port), timeout)
        except socket.error as clErr:
            raise ClientError("failed to connect", clErr)


         # with socket.socket() as connection:
         #     connection.connect((self.adr, seld.port), timeout)

    def get(self, key):
        normal_answ = 'ok'
        key_tosnd = 'get' + ' ' + str(key) + '\n'
        data_returned = {}
        data_recvd = ''
        tmp_lst = []
        try:
            self.connection.send(key_tosnd.encode())
        except socket.error as clErr:
            raise ClientError("failed to send get request", clErr)

        while not data_recvd.endswith('\n\n'):
            try:
                data_recvd += self.connection.recv(1024).decode()
            except socket.error as clErr:
                raise ClientError("failed to recieve data from get request", clErr)

        data_recvd = data_recvd[:-2]
        # print('recieved answer:\n')
        # print(data_recvd)
        tmp_lst = data_recvd.split('\n') #list of lines
        # print(tmp_lst)
        if tmp_lst[0] == normal_answ:
            for data in tmp_lst[1:]:
                # print(data.split(' '))
                if len(data.split(' ')) != 3:
                    raise ClientError("ClientError")
                else:
                    key_rcvd, value_rcvd, time_rcvd = data.split(' ') #list of keys, values and timestamps
                if key_rcvd not in data_returned:
                    data_returned[key_rcvd] = []
                try:
                    data_returned[key_rcvd].append((int(time_rcvd), float(value_rcvd),))
                except ValueError as clErr:
                    raise ClientError("value and time must be numbers", clErr)
            sorted(data_returned.items(),key=lambda values: values[1][0])
        else:
            raise ClientError("ClientError")
        return data_returned
        # except ClientError as clErr:
        #     #print(clErr)
        #     raise ClientError('ClientError', clErr)

#in data_returned values should be int and float!


    def put(self, key, value, timestamp=None):
        normal_answ = 'ok\n\n'
        if timestamp == None:
            data_to_snd = 'put' + ' ' + str(key) + ' ' + str(value) + ' '  + str(int(time.time())) + '\n'
        else:
            data_to_snd = 'put' + ' ' + str(key) + ' ' + str(value) + ' ' + str(timestamp) + '\n'
        try:
            self.connection.send(str.encode(data_to_snd)) # https://docs.python.org/3/library/stdtypes.html?highlight=str.encode#str.encode
        except socket.error as clErr:
            raise ClientError("failed to send get request", clErr)
        try:
            data_recvd = self.connection.recv(1024).decode()
        except socket.error as clErr:
            raise ClientError("failed to send get request", clErr)

        # print('recieved answer:\n')
        # print(data_recvd)
        if data_recvd == normal_answ:
            pass
        else:
            raise ClientError("ClientError")
        # except ClientError as clErr:
        #     print(clErr)

    def __del__(self):
        try:
            self.connection.close()
        except socket.error as clErr:
            raise ClientError("failed to close connection", clErr)
