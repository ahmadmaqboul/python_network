import socket
import pickle
import threading

def recive(my_info):

    UDP_IP = my_info[0] #Server IP
    UDP_PORT = my_info[1] #Server Port
    addr_list=[]
    

    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True: # make server listen all time 
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        data = pickle.loads(data)
        print(data)
        s_addr = data[1]
        
        if s_addr in addr_list : # start conv or send password 
            print("write you message here please : ")
            send(input(),my_info,data[1])

            return True

        else: # auth 
            
            a=password_request(s_addr,my_info)
            while a == False :
                a = password_request(s_addr,my_info)
    
            else :
                addr_list.append(s_addr)
                

def authntecation(password):

    if password == "password":
        return True 
    else :
        return False

def send(message, my_addr, s_addr):

    message_to_send = [message,my_addr]
    message_to_send =  pickle.dumps(message_to_send)
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(message_to_send, (s_addr[0], s_addr[1]))
    

def password_request(s_addr,my_addr):
    
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    message = ["please enter password : ",my_addr]
    message = pickle.dumps(message)
    sock.sendto(message, (s_addr[0], s_addr[1]))
    password = recive_pass(my_addr)
    return authntecation(password)


def recive_pass(my_info):

    password="password"
    return password



def file_send():
    print()




if __name__ == "__main__":
    
    my_info=["127.0.0.1",5005]
    recive(my_info)


    
