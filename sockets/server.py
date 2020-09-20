import socket
from threading import Thread
from os.path import isfile

PORT = 8800

class ClientListener(Thread):
    def __init__(self, sock):
        super().__init__(daemon=True)
        self.sock = sock
        self.file_data = b''

    def close(self):
        self.sock.close()
        print(self, ' finished')

    def init_transfer(self):
        message = b''
        while True:
            data = self.sock.recv(1024)
            print('recieved ', data)
            if b'\x00' in data: # initial message is null terminated
                last_data = data.split(b'\x00')
                data = last_data[0]
                message += data
                self.file_data = last_data[1:]
                break
            message += data
        print(f'got file name {message.decode()}')
        return message.decode()

    def gen_server_name(self, name):
        i = 1
        name_split = name.split('.')
        
        while(isfile(name)):
            if i > 255:   # safety check
                print('too many copies of the same file')
                exit(1)
                
            new_name_split = name_split.copy()
            new_name_split[0] += f'_copy{i}'  # try adding _copy{i} to the original name until 
            name = '.'.join(new_name_split)   # a fresh name is found
            i += 1
        return name


    def load_file(self, f):
        for data_bytes in self.file_data:   
            f.write(data_bytes) # write the data that arrived while transferring the file name
        while True:
            data = self.sock.recv(1024)
            print('recieved ', data)
            if data:
                f.write(data)
            else:
                break
            

    
    def run(self):
        client_name = self.init_transfer()
            
        server_name = self.gen_server_name(client_name)    
        f = open(server_name, 'wb')

        self.load_file(f)
        self.close()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('', PORT))
    sock.listen()

    while True:
        conn, addr = sock.accept()
        print(f'{str(addr)} connected')

        ClientListener(conn).start()

if __name__ == '__main__':
    main()
