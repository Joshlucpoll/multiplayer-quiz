# The socket server library is a more powerful module for handling sockets, it will help you set up and manage multiple clients in the next step
import socketserver
from collections import namedtuple
from fl_networking_tools import get_binary, send_binary

'''
Commands:
PLACE YOUR COMMANDS HERE
QUES - question command
'''

# Named tuples are extensions of the tuple structure, with contents you can refer to by name. In this case, the question will be held in a variable named q and the answer in answer.
# This is just the set up of the question - it will be sent to the client using the send_binary function when a request is made.
Question = namedtuple('Question', ['q', 'answer'])

q1 = Question("Expand the acronym ALU:", "Arithmetic Logic Unit")

# The socketserver module uses 'Handlers' to interact with connections. When a client connects a version of this class is made to handle it.
class QuizGame(socketserver.BaseRequestHandler):
    # The handle method is what actually handles the connection
    def handle(self):
        #Retrieve Command
        for request in get_binary(self.request):
            if request[0] == "QUES":
                #Send question
                send_binary(self.request, (1, q1.q))
        #Your server code goes here


# Open the quiz server and bind it to a port - creating a socket
# This works similarly to the sockets you used before, but you have to give it both an address pair (IP and port) and a handler for the server.
quiz_server = socketserver.TCPServer(('127.0.0.1', 2065), QuizGame)
quiz_server.serve_forever()