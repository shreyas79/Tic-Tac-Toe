import socket
import time
import threading
import tkinter as tk
import os
import time
import random
import pickle

board = [" " for x in range(9)]

def printBoard():
    '''prints the tic tac toe board'''
    
    
    print ( "   |   |   ")
    print (" "+board[0]+" | "+board[1]+" | "+board[2]+"  ")
    print ("   |   |")
    print ("---|---|---")
    print ("   |   |")
    print (" "+board[3]+" | "+board[4]+" | "+board[5]+"  ")
    print ("   |   |")
    print ("---|---|---")
    print ("   |   |")
    print (" "+board[6]+" | "+board[7]+" | "+board[8]+"  ")
    print ("   |   |   ")



def construct_board(board):
    '''constructs the string version of tic tac toe board to send to client'''
    
    
    line_1=         "   |   |   \n"
    line_2=line_1+  "   |   |   \n".format(board[0],board[1],board[2])
    line_3=line_2+  "   |   |   \n"
    line_4=line_3+  "---|---|---\n"
    line_5=line_4+  "   |   |   \n"
    line_6=line_5+  "   |   |   \n".format(board[3],board[4],board[5])
    line_7=line_6+  "   |   |   \n"
    line_8=line_7+  "---|---|---\n"
    line_9=line_8+  "   |   |   \n"
    line_10=line_9+ "   |   |   \n".format(board[6],board[7],board[8])
    line_11=line_10+"   |   |   \n"
    return line_11

print(construct_board(board))

host="127.0.0.1"
port=8003
server=None
clients=[]
threads=[]

def start_server():
    '''This method starts the tcp server with IPv4 configuration concurrently'''
    
    
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((host,port))
    server.listen(5)
    
    t1= threading.Thread(target=accept_connection,args=(server,))
    threads.append(t1)
    t1.start()
    #accept_connection(server)

def accept_connection(server):
    '''This method accepts the connection from the clients uses multithreading'''
    
    
    while True:
        if(len(clients)<=2):
            connection,address =server.accept()
            clients.append(connection) 
            
            t2=threading.Thread(target=send_and_receive,args=(connection,address,))
            threads.append(t2)
            t2.start()
            
            
def check_row(symbol,player):
    '''This method checks whether any rows have same markings and exits if a winner is found'''
    
    
    flag=False
    if(board[0]==board[1]==board[2]==symbol):
        flag=True
        
    elif(board[3]==board[4]==board[5]==symbol):
        flag=True
        
    elif(board[6]==board[7]==board[8]==symbol):
        flag=True
        
    if(flag):
        print("player {} won".format(player))
        for i in range(threads):
            threads[i].join()
        server.close()
        exit()
        
        

def check_col(symbol,player):
    '''This method checks whether any cols have same markings and exits if a winner is found'''
    
    
    flag=False
    if(board[0]==board[3]==board[6]==symbol):
        flag=True
        
    elif(board[1]==board[4]==board[7]==symbol):
        flag=True
        
    elif(board[2]==board[5]==board[8]==symbol):
        flag=True
        
    if(flag):
        print("player {} won".format(player))
        for i in range(threads):
            threads[i].join()
        server.close()
        exit()


def check_diagnol(symbol,player):
    '''This method checks whether the diagnols have same markings and exits if a winner is found'''
    
    
    if(board[0]==board[5]==board[8]==symbol or board[2]==board[5]==board[7]==symbol):
        print("player {} won".format(player))
        for i in range(threads):
            threads[i].join()
        server.close()
        exit()
        


#Not used currently, but can be used for multiple client architecture, needs little bit modification
def concurrent_send_and_receive(connection,address):
    '''This is the method which solely uses multithreding and supports two clients and the server acts as a delegate
    needs to be modified a little bit'''
    
    
    print("current is " ,threading.current_thread())
    
    turn="player1"
    symbols = ["O", "X"]
    
    print("waiting for player 2")
    print("starting game")
        
    count=0
    while count<9:
        
        #the switch is made according to the boolean variable
        if (turn=="player1"):
            #messages are sent and the current status of the board is sent as pickle dump
            clients[0].send("please enter the input".encode())
            clients[1].send("wait".encode())
            var=pickle.dumps(construct_board(board))
            clients[0].send(var)
            
            print("--------------------player1-------------------------")
            choice= int(clients[0].recv(1024).decode())
            
            if(0<=choice<9 and board[choice]==" "):
                #count is increased only for valid choice
                count+=1
                board[choice]=symbols[0]
                turn="player2"
        else:
            #after the move is made the table is checked for any winner can be optimized for O(1)
            check_row(symbol[0],"1")
            check_col(symbol[0],"1")
            check_diagnol(symbol[0],"1")
            time.sleep(1)
                
                
        if (turn=="player2"):
            clients[1].send("please enter the input".encode())
            clients[0].send("wait".encode())
            var=pickle.dumps(construct_board(board))
            clients[1].send(var)
            print("---------------------player2------------------------")

            choice= int(clients[1].recv(1024).decode())
            print("p2",choice)
            if(0<=choice<9 and board[choice]==" "):
                count+=1
                board[choice]=symbols[1]
                turn="player1"    
        else:
            
            check_row(symbol[1],"2")
            check_col(symbol[1],"2")
            check_diagnol(symbol[1],"2")
            time.sleep(1)
    else:
        print("Match Drawn")


def send_and_receive(connection,address):
    '''This is the method which uses the main class as a player and a single client seems to be working but has issues
    regarding compatability'''
    symbols=["O","X"]
    count=0
    while(count<9):
        
        while(True):
            
            var=pickle.dumps(construct_board(board))
            clients[0].sendall(var)
            clients[0].sendall("please enter the input".encode())
            choice= int(clients[0].recv(1024).decode())
            print("choice is ",choice)
            
            if(0<=choice<9 and board[choice]==" "):
                
                count+=1
                board[choice]=symbols[1]
                check_row(symbols[1],"2")
                check_col(symbols[1],"2")
                check_diagnol(symbols[1],"2")
                break
        
        while(True):
            
            clients[0].send("wait".encode())
            printBoard()
            choice=""
            
            try:
                choice=input("please enter the input")
            except :
                print(choice)
                
            if(0<=choice<9 and board[choice]==" "):
                
                count+=1
                board[choice]=symbols[0]
                check_row(symbols[1],"1")
                check_col(symbols[1],"1")
                check_diagnol(symbols[1],"1")
                break
            
            
            
 start_server()