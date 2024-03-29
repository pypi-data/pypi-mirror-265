import socket
import threading
import time
import zlib
import traceback
from datetime import datetime

from .data.message_data import MessageData
from .interface import MsgID


class TSocket(object):
    __instance = None

    def __init__(self):
        self.__HOST = '127.0.0.1'
        self.__PORT = 12321
        self.__ADDR = (self.__HOST, self.__PORT)
        self.__TCP_SOCKET = None
        self.__RECV_T = None
        self.__RECV_BYTES = b''
        self.__BASE_CALLBACK = None
        self.__CHART_CALLBACK = None
        self.__MARKET_CALLBACK = None
        self.__TRADE_CALLBACK = None
        self.__SessionInited = False
        self.__IsRunning = False
        self.__last_recv_time = -1

    def __del__(self):
        self.__BASE_CALLBACK = None
        self.__CHART_CALLBACK = None
        self.__MARKET_CALLBACK = None
        self.__TRADE_CALLBACK = None
        self.close()

    def set_base_callback(self, base_callback):
        self.__BASE_CALLBACK = base_callback

    def set_chart_callback(self, chart_callback):
        self.__CHART_CALLBACK = chart_callback

    def set_market_callback(self, market_callback):
        self.__MARKET_CALLBACK = market_callback

    def set_trade_callback(self, trade_callback):
        self.__TRADE_CALLBACK = trade_callback

    def close(self):
        self.__IsRunning = False
        if self.__TCP_SOCKET is not None:
            self.__TCP_SOCKET.close()
        if self.__RECV_T is not None:
            self.__RECV_T.join()
        self.__RECV_T = None
        self.__TCP_SOCKET = None

    def is_connected(self):
        return self.__TCP_SOCKET is not None and self.__TCP_SOCKET._closed is False

    def connect(self, host: str = None, port: int = None, timeout: int = 30000):
        if self.is_connected() is True:
            return [True, '']

        if host is not None:
            self.__HOST = host
        if port is not None:
            self.__PORT = port
        self.__ADDR = (self.__HOST, self.__PORT)
        try:
            if self.__TCP_SOCKET is None:
                self.__TCP_SOCKET = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
                self.__TCP_SOCKET.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                self.__TCP_SOCKET.setblocking(False)
            self.__TCP_SOCKET.settimeout(int(timeout / 1000))

            self.__TCP_SOCKET.connect(self.__ADDR)
        except socket.error as e:
            self.close()
            traceback.print_exc()
            return [False, e.strerror]

        if self.__RECV_T is None:
            self.__IsRunning = True
            self.__RECV_T = threading.Thread(target=self.__recv_data)
            self.__RECV_T.start()

        while True:
            if self.__SessionInited is True:
                return [True, '']
            time.sleep(0.5)

        return [True, '']

    def send_message(self, msg: MessageData):
        if self.is_connected() is False:
            return False
        if len(msg.UData) > 102400:
            msg.CompressType = 0
            compressed = zlib.compress(msg.UData, -1)
            msg.UData = len(compressed).to_bytes(4, 'big') + compressed

        msgp = msg.pack()
        sendbytes = len(msgp).to_bytes(4, 'little') + msgp

        self.__TCP_SOCKET.sendall(sendbytes)
        return True

    def __recv_data(self):
        while self.__IsRunning:
            if self.is_connected() is False:
                break
            try:
                recv_data = self.__TCP_SOCKET.recv(10000000)
                self.__RECV_BYTES += recv_data
                if len(recv_data) > 0:
                    self.__last_recv_time = int(datetime.now().timestamp())

            except Exception as e:
                if self.__IsRunning is True:
                    self.__TCP_SOCKET.close()
                    traceback.print_exc()
                return [False, e]

            try:
                sz = int.from_bytes(self.__RECV_BYTES[:4], byteorder='little')
                while len(self.__RECV_BYTES) >= sz + 4:
                    msg_bytes = self.__RECV_BYTES[4:sz + 4]
                    self.__notify_msg(msg_bytes)
                    self.__RECV_BYTES = self.__RECV_BYTES[sz + 4:]
                    sz = int.from_bytes(self.__RECV_BYTES[:4], byteorder='little')
            except Exception as e:
                self.__TCP_SOCKET.close()
                traceback.print_exc()
                return [False, e]

            nowts = int(datetime.now().timestamp())
            if self.__last_recv_time > 0 and nowts - self.__last_recv_time > 3:
                msg = MessageData(mid=int(MsgID.MSGID_Base_Heart.value))
                self.send_message(msg=msg)
            time.sleep(0.001)

    def __notify_msg(self, msg_bytes):
        msg = MessageData()
        if msg.un_pack(msg_bytes) is True:
            if msg.CompressType == 0:
                msg.UData = zlib.decompress(msg.UData)
            if msg.MID >= 1000 and msg.MID < 2000:
                if msg.MID == int(MsgID.MSGID_Base_SessionInit.value):
                    self.__SessionInited = True
                    return
                if self.__BASE_CALLBACK is not None:
                    self.__BASE_CALLBACK(msg)
            elif msg.MID >= 200000 and msg.MID < 300000:
                if self.__MARKET_CALLBACK is not None:
                    self.__MARKET_CALLBACK(msg)
            elif msg.MID >= 300000 and msg.MID < 400000:
                if self.__TRADE_CALLBACK is not None:
                    self.__TRADE_CALLBACK(msg)
            elif msg.MID >= 400000 and msg.MID < 500000:
                if self.__CHART_CALLBACK is not None:
                    self.__CHART_CALLBACK(msg)
        else:
            print('unpack errror')
