import asyncore
import socket
import mysql_conn

#address='192.168.67.30'
address='192.168.100.254'

def decode_data(data):
    decoded=data.decode("utf-8")
    decoded=decoded.replace("'","")
    decoded=decoded.split(',')
    decoded=[x.strip() for x in decoded]
    return decoded

def insert_into_db(data):
    print('ok')

class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            try:
                decoded=decode_data(data)
                if int(decoded[0])<5:
                    mysql_conn.insert_sensordata_db(decoded)
                    self.send(data)
                else:
                    print(decoded)
            except:
                print(decoded)

class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print ('Incoming connection from %s' % repr(addr))
            handler = EchoHandler(sock)

def main_loop():
    server = EchoServer(address, 8090)
    asyncore.loop()

if __name__ == "__main__":
    main_loop()
