import socket
import time


class ClientError(Exception):
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
        tmp_lst = data_recvd.split('\n') #list of lines

        if tmp_lst[0] == normal_answ:
            for data in tmp_lst[1:]:
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
            # https://stackoverflow.com/questions/3121979/how-to-sort-a-list-tuple-of-lists-tuples-by-the-element-at-a-given-index
            for values in data_returned.values():
                values.sort(key=lambda tuple: tuple[0])
        else:
            raise ClientError("ClientError")
        return data_returned

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

        if data_recvd == normal_answ:
            pass
        else:
            raise ClientError("ClientError")

    def __del__(self):

        try:
            self.connection.close()
        except socket.error as clErr:
            raise ClientError("failed to close connection", clErr)

''' solution

import bisect
import socket
import time


class ClientError(Exception):
    """класс исключений клиента"""
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

        try:
            self.connection = socket.create_connection((host, port), timeout)
        except socket.error as err:
            raise ClientError("Cannot create connection", err)

    def _read(self):

        data = b""

        while not data.endswith(b"\n\n"):
            try:
                data += self.connection.recv(1024)
            except socket.error as err:
                raise ClientError("Error reading data from socket", err)

        return data.decode('utf-8')

    def _send(self, data):

        try:
            self.connection.sendall(data)
        except socket.error as err:
            raise ClientError("Error sending data to server", err)

    def put(self, key, value, timestamp=None):

        timestamp = timestamp or int(time.time())
        self._send(f"put {key} {value} {timestamp}\n".encode())
        raw_data = self._read()

        if raw_data == 'ok\n\n':
            return
        raise ClientError('Server returns an error')

    def get(self, key):

        self._send(f"get {key}\n".encode())
        raw_data = self._read()
        data = {}
        status, payload = raw_data.split("\n", 1)
        payload = payload.strip()

        if status != 'ok':
            raise ClientError('Server returns an error')

        if payload == '':
            return data

        try:

            for row in payload.splitlines():
                key, value, timestamp = row.split()
                if key not in data:
                    data[key] = []
                bisect.insort(data[key], ((int(timestamp), float(value))))

        except Exception as err:
            raise ClientError('Server returns invalid data', err)

        return data

    def close(self):

        try:
            self.connection.close()
        except socket.error as err:
            raise ClientError("Error. Do not close the connection", err)
            '''
