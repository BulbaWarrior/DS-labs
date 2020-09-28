from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime
from time import sleep

names = ['a', 'b', 'c'] # a small kostyl to translate "pids" to process names


def local_time(counter):
    return f'(LAMPORT_TIME={counter}, LOCAL_TIME={datetime.now()})'


def calc_recv_timestamp(recv_time_stamp, counter):
    for i in range(len(counter)):
        counter[i] = max(counter[i], recv_time_stamp[i])
    return counter

def event(pid, counter):
    counter[pid] += 1
    print(f'Internal event in {names[pid]} {local_time(counter)}')
    return counter

def send_message(pipe, pid, counter):
    counter[pid] += 1
    pipe.send(('Message content', counter))
    print(f'Message sent from {names[pid]} {local_time(counter)}')
    return counter

def recv_message(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    counter[pid] += 1
    print(f'Message received at {names[pid]} {local_time(counter)}')
    return counter

def print_final_state(pid, counter):
    print(f'Process {names[pid]} {counter}')

def process_one(pipe12):
    pid = 0
    counter = [0, 0, 0]
    counter = send_message(pipe12, pid, counter)
    counter = send_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)
    sleep(0.1)
    print_final_state(pid, counter)


def process_two(pipe21, pipe23):
    pid = 1
    counter = [0, 0, 0]
    counter = recv_message(pipe21, pid, counter)
    counter = recv_message(pipe21, pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = recv_message(pipe23, pid, counter)
    counter = event(pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = send_message(pipe23, pid, counter)
    counter = send_message(pipe23, pid, counter)
    sleep(0.2)
    print_final_state(pid, counter)

def process_three(pipe32):
    pid = 2
    counter = [0, 0, 0]
    counter = send_message(pipe32, pid, counter)
    counter = recv_message(pipe32, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe32, pid, counter)
    sleep(0.3)
    print_final_state(pid, counter)



def main():
    pipe12, pipe21 = Pipe()
    pipe23, pipe32 = Pipe()

    process1 = Process(target=process_one, args=(pipe12,))

    process2 = Process(target=process_two, args=(pipe21, pipe23))

    process3 = Process(target=process_three, args=(pipe32,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()


if __name__ == '__main__':
    main()
