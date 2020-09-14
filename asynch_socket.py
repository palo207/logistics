import asyncore
import socket
import mysql_conn

address='192.168.67.30'
workplaces=["WP1","WP2","WP3"]
#address='192.168.100.254'

def decode_data(data):
    decoded=data.decode("utf-8")
    decoded=decoded.replace("'","")
    decoded=decoded.split(',')
    decoded=[x.strip() for x in decoded]
    return decoded

def get_row(data):
    row= ";"+" , ".join(str(x) for x in data)+",+"
    print(row)
    return row

class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            try:
                decoded=decode_data(data)
                if decoded[0] in workplaces and len(decoded)==1:
                    data=mysql_conn.read_bom_from_db(decoded[0])
                    for i in range(len(data)):
                        row=get_row(data[i])
                        self.send(row.encode())

                if decoded[0]=="buf":
                    print("Fetching buffer status for {}".format(decoded[1]))
                    data=mysql_conn.read_buffer_status(decoded[1])
                    data=[data[0][0],data[1][0],data[2][0]]
                    row=get_row(data)
                    self.send(row.encode())

                if decoded[0]=="upd":
                    print("Update coming up")
                    mysql_conn.update_buffer_status(decoded)

                if int(decoded[0])<8:
                    mysql_conn.insert_sensordata_db(decoded)
                    #self.send(data)
                else:
                    print(decoded)
            except:
                print(data)

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
