import socket
import pickle
import threading

def recive(my_info,rec_intry): #tis is the main function reciving the data 

    UDP_IP = my_info[0] #Server IP
    UDP_PORT = my_info[1] #Server Port
    addr_list=[] #list have only the auth users 
    addr_list.append(rec_intry)
    
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True: # make server listen all time 
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        data = pickle.loads(data)
        s_addr = data[1] #sender addrese in this form  -> [127.0.0.1,5005]
        
        if s_addr in addr_list and data[0]!="file_transfer:" : # start conv or send password 
            print("message from",s_addr,":",data[0])
            print("if you want to file transfer please type (file_transfer:)")
            print("write your message here : ") # make user send a message to the sender 
            message_to_send = input()
            
            if message_to_send=="file_transfer:":
                message=pickle.dumps([message_to_send,my_info])
                sock.sendto(message,(s_addr[0],s_addr[1]))
                file = open("file path you want to send", "rb")
                SendData = file.read(1024)
                SendData=pickle.dumps(SendData)

                while SendData:
                    # Now we can receive data from server
                    print("\n\n################## Below message is received from server ################## \n\n ")
                    #Now send the content of sample.txt to server
                    sock.sendto(SendData,(rec_info[0],rec_info[1]))
                    SendData = file.read(1024)
                send_to_server(my_info,rec_info)
                    
            else:
                message=pickle.dumps([message_to_send,my_info])
                sock.sendto(message,(s_addr[0],s_addr[1]))

        
        elif s_addr in addr_list and data[0]=="file_transfer:":
            
            f = open("PATH FILE where you want to save file", "wb") 
            print("\n Copied file name will be rec.txt at peer 1 side\n")

                # Receive any data from client side
            data1 = sock.recvfrom(1024)
            print(data1)
            datas=pickle.loads(data1[0])
            print(datas)
            f.write(datas)
            #Close the file opened at server side once copy is completed
            f.close()
            print("\n File has been copied successfully \n")

        else: # auth 
            req_password=password_request(data,s_addr,my_info)
            if req_password == False :
                print("waitting for password ..")
    
            else :
                addr_list.append(s_addr)

def password_request(data,s_addr,my_addr): # if password false send to retype it 
    
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    message = ["please enter password : ",my_addr]
    message = pickle.dumps(message)
    sock.sendto(message, (s_addr[0], s_addr[1]))
    password = data[0]
    return authntecation(password)

def authntecation(password):#check if password true or not (we can use enc algo depend on public and private key)

    if password == "password":
        return True 
    else :
        return False
        
def send_to_server(my_info,rec_info):
    print("please enter your message")
    message_to_send=input()
    message=pickle.dumps([message_to_send,my_info])
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.sendto(message,(rec_info[0],rec_info[1]))


if __name__ == "__main__":
    
    my_info=["127.0.0.1",5005]# your ip and port 
    rec_info=["127.0.0.1",6005]# peer you want to communicate with 
    empty_list=1

    print("do you want to start chat or only listing ? if you want to start chat -> 1 no -> 2")
    
    choose=int(input())
    
    if choose == 1 :
        y = threading.Thread(target=send_to_server(my_info,rec_info))
        x = threading.Thread(target=recive(my_info,rec_info))
        y.start()
        x.start()
    
    elif choose == 2 :
        x = threading.Thread(target=recive(my_info,empty_list))
        x.start()
    
    else:
        print("exit")




    





    
