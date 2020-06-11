# The socket server library is a more powerful module for handling sockets, it will help you set up and manage multiple clients in the next step
import socketserver
from collections import namedtuple
from fl_networking_tools import get_binary, send_binary
from threading import Event
import time
'''
Commands:
PLACE YOUR COMMANDS HERE
JOIN - request to join
QUES - question command
ANS - answer command
'''
global NUMBER_OF_PLAYERS, players, scores, questions, ready_to_start, everyone_finished

NUMBER_OF_PLAYERS = 2
players = []
scores = {}

Question = namedtuple('Question', ['q', 'answer'])
questions = [
    Question("What is the name of the bounty hunter who captured Han Solo in The Empire Strikes Back?", "Boba Fett"),
    Question("What colour was Qui-Gon Jinn’s lightsaber?", "Green"),
    Question("In The Empire Strikes Back, Lando Calrissian is the Baron Administrator of Cloud City on which planet?", "Bespin"),
    Question("Jar Jar Binks belongs to what species?", "Gungan"),
    Question("In what year was the first installment of the Star Wars: Battlefront video game series released?", "2004")
]


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class QuizGame(socketserver.BaseRequestHandler):
    def setup(self):
        self.startTime = 0
        self.endTime = 0
        self.currentQuestion = 0
        self.attempts = 0
        self.score = 0

    def handle(self):
        global players, NUMBER_OF_PLAYERS, scores, questions, ready_to_start, everyone_finished
        
        for request in get_binary(self.request):
            
            if request[0] == "JOIN":
                
                if len(players) >= NUMBER_OF_PLAYERS:
                    send_binary(self.request, [1, ""]) # game full
                else:
                    self.teamName = request[1]
                    players.append(self.teamName)
                    send_binary(self.request, [2, ""]) # game not full
                    
                    if len(players) == NUMBER_OF_PLAYERS:
                        # Starts Game
                        ready_to_start.set()
                    else:
                        amountOfPlayers = str(len(players)) + "/" + str(NUMBER_OF_PLAYERS)
                        send_binary(self.request, [3, amountOfPlayers]) # waiting for other players
                        # Waits until all player have connected
                        ready_to_start.wait()
                    
                    send_binary(self.request, [4, ""]) # Game started
                    self.startTime = time.time()


            if request[0] == "QUES":
                if self.currentQuestion >= len(questions):
                    # Calculate timetaken
                    self.endTime = time.time()
                    timeTaken = self.endTime - self.startTime
                    send_binary(self.request, [9, round(timeTaken, 2)]) # Send Game end

                    scores[self.teamName] = self.score
                    if len(scores) == NUMBER_OF_PLAYERS:
                        everyone_finished.set()
                    else:
                        everyone_finished.wait()
                    
                    sortedScores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                    send_binary(self.request, [10, sortedScores])
                        

                else:
                    send_binary(self.request, [5, questions[self.currentQuestion].q])


            if request[0] == "ANS":
                
                if request[1].lower() == questions[self.currentQuestion].answer.lower(): 
                    send_binary(self.request, [6, ""]) # Correct ans
                    self.score += 6 / (self.attempts + 1)
                    self.currentQuestion += 1
                    self.attempts = 0

                elif self.attempts < 2:
                    send_binary(self.request, [7, ""]) # Incorrect attempt
                    self.attempts += 1
                    
                else:
                    send_binary(self.request, [8, questions[self.currentQuestion].answer]) # Incorrect ans
                    self.currentQuestion += 1
                    self.attempts = 0
                    


ready_to_start = Event()
everyone_finished = Event()
quiz_server = ThreadedTCPServer(('127.0.0.1', 2065), QuizGame)
quiz_server.serve_forever()