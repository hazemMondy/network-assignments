"""client.py"""
import socket
import random
import time

# constants
HEADER = 1024
PORT = 3006
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

"params"
ERR_PROP = .3
TIMEOUT = 0.0045
window = 2
TIMOUTTIMERS = []
buffer = [None]*window

"socket"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def error(seq:int)->int:
    """miss with the sequence
    if noise is bigger than usual
    """
    out = seq
    if ERR_PROP > random.random():
        out=seq+1
    return out

def packet(msg:str)->list:
    """
    divide message
    """
    # do not omit spaces
    message_list = list(msg)
    return message_list

def send_and_check_time( msg:str,seq:int ) ->(str,float):
    """
    send , recieve , calc the time to response
    """
    #add error
    seq = error(seq)
    message = (str(seq)+msg).encode(FORMAT)
    client.send(message)
    response_time_str = time.perf_counter()
    response = client.recv(1024).decode(FORMAT)
    response_time_end = time.perf_counter()
    response_time = response_time_str-response_time_end
    return response,response_time

# just send
def send( msg:str,seq:int)->None:
    """
    concate the message with seq/error
    """
    #add error
    seq = error(seq)
    message = (str(seq)+' '+msg).encode(FORMAT)
    client.send(message)

def check_nack(msg:str)->bool:
    """NACK"""
    return (True if msg=="N" else False)

def check_ack(msg:str)->bool:
    """ACK"""
    return (True if msg!="N" else False)

def sendii(message_list:list)->None:

    """the for loop act like a buffer
    we send one by one  -> window = 1"""
    for seq,i in enumerate(message_list):
        #resend until it is ack
        while True:
            #timming for one
            #it's non sense it will allways send to server
            #"""so we will make random time before sending and see if
            #it exceeds the timeout before sending
            #"""
            rand = random.uniform(0.0,TIMEOUT*1.5001)
            if rand < TIMEOUT:
                send(i,seq)
                TIMOUTTIMERS[seq]=time.perf_counter()
                response = client.recv(1024).decode(FORMAT)
                response_time_end = time.perf_counter()
                response_time = response_time_end - TIMOUTTIMERS[seq]
                print(response," ", f'{(response_time):0.5f} s')
                if check_ack(response[0]):
                    break
            else :
                print("TIMEOUT"," seq ", seq," " , f'{(rand):0.5f} s')

def send_buffer(message_list:list,window:int):

    """
    we have a buffer
    send with max sequence =1
    window
    """
    current_sequence = 0
    last_window = window
    length= len(message_list)
    responses =[None]*length

    # whole message
    while current_sequence<last_window-1 :
        #buffer=message_list[current_sequence:current_sequence+last_window-1]
        ack_flag= False
        rand = random.uniform(0.0,TIMEOUT*1.5001)
        timeout = (rand < TIMEOUT)

        if timeout:
            ack_flag=True
            # send from current all the window
            for i in range(last_window-current_sequence):
                if current_sequence+i < length:
                    send(message_list[current_sequence+i] , current_sequence+i)

                    TIMOUTTIMERS[current_sequence+i]=time.perf_counter()
                    response = client.recv(1024).decode(FORMAT)
                    endtime=time.perf_counter()
                    responses[current_sequence+i] = endtime - TIMOUTTIMERS[current_sequence+i]
                    print(response," ", f'{(responses[current_sequence+i]):0.5f} s')
                    if check_nack(response[0]):
                        # resend
                        current_sequence +=i
                        last_window=( last_window+i if last_window<(length-1) else last_window)
                        ack_flag=False
                        break
        else :
            print("TIMEOUT"," seq ", current_sequence," " , f'{(rand):0.5f} s')
        #updates
        if ack_flag and timeout:
            # all went good
            current_sequence += window
            last_window=( last_window + window if last_window<(length-1-window) else length)
        ack_flag = True
    return

def main():
    "main"
    global TIMOUTTIMERS
    global window
    global ERR_PROP
    global TIMEOUT

    message="ASU NETWORKs"
    #message=str(input())
    #window = int(input())
    #TIMEOUT = float((input()))
    #ERR_PROP = float(input())
    msg = packet(message)
    TIMOUTTIMERS = [0 for i in range(len(msg))]
    send_buffer(msg, window)
    print("Transacation complete!")
    return

if __name__ == '__main__':
    main()
