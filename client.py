import socket
import pickle
# Import the functions from the networking tools module
from fl_networking_tools import get_binary, send_binary

'''
Responses
LIST YOUR RESPONSE CODES HERE
0 - Initalision
1 - Game full
2 - Game not full
3 - Waiting for other players
4 - Quiz in progress
5 - Question
6 - Correct answer
7 - Incorrect answer
8 - Quiz stopped
9 - Results data
'''

# A flag used to control the quiz loop.
playing = True

IP = input("What is the IP address of the server:\n")
if IP == "":
    IP = "127.0.0.1"

teamName = input("What is your team name?\n")
print("\nWelcome " + teamName)
print("Connecting to Server\n")

quiz_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

quiz_server.connect((IP, 2065))

print("Connected\n")
# Sending a command to the server.
send_binary(quiz_server, ["QUES", ""])

while playing:
    # The get_binary function returns a list of messages - loop over them
    for response in get_binary(quiz_server):
        # response is the command/response tuple - response[0] is the code
        if response[0] == 1: # The question response
            # Display it to the user.
            print(response[1])
            answer = input("")
