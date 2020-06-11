import socket
import pickle
from fl_networking_tools import get_binary, send_binary
import time

'''
Responses
LIST YOUR RESPONSE CODES HERE
1 - Game full
2 - Game not full
3 - Waiting for other players
4 - Quiz starting
5 - Question
6 - Correct answer
7 - Incorrect attempt
8 - Incorrect answer
9 - Quiz finished
10 - Results data
'''

def connectToServer(IP):
    quiz_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    quiz_server.connect((IP, 2065))
    return quiz_server

playing = True

IP = input("What is the IP address of the server:\n")
if IP == "":
    IP = "127.0.0.1"

teamName = input("What is your team name?\n")
print("\nWelcome " + teamName)
print("Connecting to Server\n")

quiz_server = connectToServer(IP)

send_binary(quiz_server, ["JOIN", teamName])


while playing:
    for response in get_binary(quiz_server):
        
        if response[0] == 1: # Game full
            disconnectFromServer(quiz_server)
            print("The lobby is full, please try again later :(")
            playing = False

        if response[0] == 2: # Game not full
            print("Connected\n")

        if response[0] == 3: # Waiting for other players
            print("Waiting for other players. Players connected:\n" + response[1])
        
        if response[0] == 4: # Game startting
            send_binary(quiz_server, ["QUES", ""])

        if response[0] == 5: # The question response
            # Display it to the user.
            print("\n" + response[1])
            answer = input()
            send_binary(quiz_server, ["ANS", answer])
        
        if response[0] == 6: # correct ans
            print("\nYou go that question right!")
            send_binary(quiz_server, ["QUES", ""])

        if response[0] == 7: # incorrect attempt
            print("\nSorry you got that question wrong...")
            print("Try again")
            send_binary(quiz_server, ["QUES", ""])

        if response[0] == 8: # incorrect ans
            print("\nSorry you got that question wrong...")
            print("The correct answer was ", response[1])
            send_binary(quiz_server, ["QUES", ""])
        
        if response[0] == 9: # Quiz finished
            print("\nYou have completed all the questions in " + str(response[1]) + " seconds.")
            print("Waiting for other players")

        if response[0] == 10: # results data
            print("\nThe winner is:")
            time.sleep(3)
            scores = response[1]
            print(str(scores[0][0]) + " with " + str(scores[0][1]) + " points!")

            time.sleep(1)
            print("\nLeaderBoard:")
            for i in scores:
                print(i[0], i[1])
            