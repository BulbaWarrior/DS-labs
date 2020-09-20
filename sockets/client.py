import socket
from sys import argv
import os


class FileSender:
    def __init__(self, sock, fname, chunk_size=1024):
        self.file_size = os.stat(fname).st_size
        self.fd = open(fname, 'rb')
        self.server_name = fname.split('/')[-1]  # I assume that all the files should be
                                             # saved to the same directory on the server
        self.sock = sock
        self.chunk_size = chunk_size

    def init_transfer(self):
        self.sock.sendall(self.server_name.encode() + b'\x00') # name is null terminated


    def send_file(self):
        chunk = self.fd.read(self.chunk_size)
        sent = 0

        while chunk: # there's still something to send
            self.sock.sendall(chunk)
            sent += len(chunk)
            print(f'sent {int((sent/self.file_size) * 100)}% of the file', end='\r')
            chunk = self.fd.read(self.chunk_size)

    def close(self):
        self.sock.close()
            
            



def main():
    if len(argv) != 4:
        print(f'usage: {argv[0]} <file> <address> <port>')
        exit()

    port = argv[3]
    host = socket.gethostbyname(argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, int(port)))
    client_fname = argv[1]

    sender = FileSender(sock, client_fname)
    sender.init_transfer()
    sender.send_file()
    sender.close()
    

if __name__ == '__main__':
    main()
