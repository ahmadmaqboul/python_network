import socket
import pickle
import threading

def recive(my_info): #tis is the main function reciving the data 

    UDP_IP = my_info[0] #Server IP
    UDP_PORT = my_info[1] #Server Port
    addr_list=[] #list have only the auth users 
    
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    message=pickle.dumps([input(),my_info])
    sock.bind((UDP_IP, UDP_PORT))

    while True: # make server listen all time 
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        data = pickle.loads(data)
        s_addr = data[1] #sender addrese in this form  -> [127.0.0.1,5005]
        
        if s_addr in addr_list : # start conv or send password 
            print("message from",s_addr,":",data[0])
            print("write you message here please : ") # make user send a message to the sender 
            message=pickle.dumps([input(),my_info])
            sock.sendto(message,(s_addr[0],s_addr[1]))
            

        else: # auth 
            a=password_request(s_addr,my_info)
            while a == False :
                a = password_request(s_addr,my_info)
    
            else :
                addr_list.append(s_addr)
                

def authntecation(password):#check if password true or not (we can use enc algo depend on public and private key)

    if password == "password":
        return True 
    else :
        return False

def send(message, my_addr, s_addr):

    message_to_send = [message,my_addr]
    message_to_send =  pickle.dumps(message_to_send)
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(message_to_send, (s_addr[0], s_addr[1]))
    

def password_request(s_addr,my_addr): # if password false send to retype it 
    
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    message = ["please enter password : ",my_addr]
    message = pickle.dumps(message)
    sock.sendto(message, (s_addr[0], s_addr[1]))
    password = recive_pass(my_addr)
    return authntecation(password)


def recive_pass(my_info): # this function must use to get the password from user if password false

    password="password"
    return password


def file_send():
    print()



if __name__ == "__main__":
    my_info=["127.0.0.1",5005]
    x = threading.Thread(target=recive(my_info))
    x.start()






    
