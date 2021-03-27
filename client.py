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

        self.connection = socket.create_connection((self.adr, self.port), timeout)

         # with socket.socket() as connection:
         #     connection.connect((self.adr, seld.port), timeout)

    def get(self, key):
        normal_answ = 'ok'
        key_tosnd = 'get' + ' ' + str(key) + '\n'
        data_returned = {}
        tmp_lst = []
        self.connection.send(key_tosnd.encode())
        try:
            data_recvd = self.connection.recv(1024).decode()[:-2]
            if len(data_recvd) == 2 and data_recvd != normal_answ:
                raise ClientError("ClientError")

            if len(data_recvd) == 2 and data_recvd == normal_answ:
                return data_returned
            # print('recieved answer:\n')
            # print(data_recvd)
            tmp_lst = data_recvd.split('\n') #list of lines
            # print(tmp_lst)
            if tmp_lst[0] != normal_answ:
                raise ClientError("ClientError")
            else:
                for data in tmp_lst[1:]:
                    tmp_answ_lst = data.split(' ') #list of keys, values and timestamps
                    data_returned[tmp_answ_lst[0]] = []

                for data in tmp_lst[1:]:
                    tmp_answ_lst = data.split(' ')
                    data_returned[tmp_answ_lst[0]].append((int(tmp_answ_lst[2]), float(tmp_answ_lst[1]),))
                sorted(data_returned.items(),key=lambda values: values[1][0])
                return data_returned
        except ClientError as clErr:
            print(clErr)

#in data_returned values should be int and float!


    def put(self, key, value, timestamp=None):
        normal_answ = 'ok\n\n'
        if timestamp == None:
            data_to_snd = 'put' + ' ' + str(key) + ' ' + str(value) + ' '  + str(int(time.time())) + '\n'
        else:
            data_to_snd = 'put' + ' ' + str(key) + ' ' + str(value) + ' ' + str(timestamp) + '\n'
        try:
            self.connection.send(str.encode(data_to_snd)) # https://docs.python.org/3/library/stdtypes.html?highlight=str.encode#str.encode
            data_recvd = self.connection.recv(1024).decode()
            # print('recieved answer:\n')
            # print(data_recvd)
            if data_recvd != normal_answ:
                raise ClientError("ClientError")
        except ClientError as clErr:
            print(clErr)

    def __del__(self):
        self.connection.close()
