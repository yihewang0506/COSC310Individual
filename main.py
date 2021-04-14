import random

import requests

import generate as gen
import preprocessing as prep

question, answer = prep.loadCorpora()
print("preparing system.....")
embeddingList = gen.wordEmbedding(question)
print("The chatbot is ready, Enter 'bye' to exit the system")
print("Hi I'm your chatbot let's chat!!")


def makereply(userinput):
    if userinput == "bye":
        # print("bye")
        listBye = ['see you', 'bye', 'bye-bye', 'good bye']
        replyBye = random.choice(listBye)
        return replyBye
    elif userinput == "hi" or userinput == "hello":
        # print("Hi!!")
        listHi = ['Hi!!', 'Hello!!', 'good to see you!', 'Hi there!']
        replyHi = random.choice(listHi)
        return replyHi
    else:
        return gen.generate(userinput, embeddingList, answer)
