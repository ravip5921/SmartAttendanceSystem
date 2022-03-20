import struct
import json


def readall(_socket):
    # read all data from socket as defined in the header
    headerlength1 = _socket.recv(1)
    headerlength2 = _socket.recv(1)
    headerlength = struct.unpack(
        '>H', headerlength1 + headerlength2)  # big endian format
    read_buffer = b''
    remaining_bytes = headerlength[0]
    while remaining_bytes > 0:
        buff = _socket.recv(remaining_bytes)
        read_buffer += buff
        remaining_bytes -= len(buff)
    data = json.loads(read_buffer)
    return data


def convert2send(data):
    # json formatted data preceded by two byte data-length and no header
    datastr = json.dumps(data)
    datalen = struct.pack('>H', len(datastr))
    datastr = datalen + datastr.encode()
    return datastr


def convertAndSend(data, sock):
    # json formatted data preceded by two byte data-length and no header
    datastr = json.dumps(data)
    datalen = struct.pack('>H', len(datastr))
    datastr = datalen + datastr.encode()
    sock.sendall(datastr)


def convertSendClose(data, sock):
    # json formatted data preceded by two byte data-length and no header
    datastr = json.dumps(data)
    datalen = struct.pack('>H', len(datastr))
    datastr = datalen + datastr.encode()
    sock.sendall(datastr)
    sock.close()
