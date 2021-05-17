# Tic-Tac-Toe

The repository consists of two files server.py and client.py, As of now server.py handles the business logic after pondering over various architectural designs, keeping the time constraints in mind, I went for this simple design paridgm <br />

**Server.py**<br /><br />
server.py contains the socket initialisation and multi threading environment to handle multiple clients, it contains the tic tac toe board and the response from the client is noted down here and checked for victory, there are two types of connection one is purely multithreaded and supports multiple clients and in this case the business logic can be moved to client but needs work, and the other one contains the player code and communication code in the server itself<br />

**Client.py**<br />
A simple client file, which connects to socket and communicates with server as well as user<br />

**Future Work**<br />
*Better the architecture so as to the business logic lies in the client, which does not make a difference in speed in applications like theese , but is a better design standard considering the high computing power of devices these days <br />
*Modify the existing code to work completely for all the cases<br />
*Front end using simple library called tkinter<br />
*Better exception handling <br />
*Update the requirements.txt <br />
*Few of the code can be efficiently implmented say O(1)<br />


**ISSUES**<br />

The client was not receivng the messages from socket, tried debugging but I think its browser or jupyter configuration issue, will look into it
have attached screenshots

