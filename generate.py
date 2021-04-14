import json
import operator
import random

import en_core_web_lg
import requests
import wikipedia
 
import preprocessing as prep

# app id for wolfram api
# notice: the max query numbers is 2000 per month for non-commercial usage
WOLFRAM_APP_ID = '9LU64T-GXWEKYXV7J'


def preprocess(sentence):  # preprocess the sentence using preprocessing model
    clean = prep.cleanPunctuationAndLower(sentence)
    stemm = prep.StemmingAndLemmatization(clean)
    spell = prep.cleanStopWordsAndSpelling(stemm)
    return spell


def wordEmbedding(question):  # change all questions in the corpora to vectors and store in a list
    embeddingList = []
    nlp = en_core_web_lg.load()

    for x in range(len(question)):
        doc = nlp(preprocess(question[x]))
        pre = [doc]
        pre.append(prep.findsenti(question[x]))  # also include the sentiment
        embeddingList.append(pre)
    return embeddingList


def generate(intputSen, doc2, answer):
    index = 0
    # get definition from Wikipedia
    if intputSen.find('ask wikipedia about') >= 0:
        userinput = intputSen.split('ask wikipedia about')[1].strip()
        # print('wikipedia api:' + userinput)
        try:
            r = wikipedia.summary(userinput)
            # make sure the length of message is less than socket buffer size
            if len(r) > 1024:
                r = r[:1024]
            while len(r) > 0 and not r.endswith('.'):
                r = r[:-1]
        except wikipedia.exceptions.DisambiguationError as e:
            r = str(e)
        except wikipedia.exceptions.PageError as pe:
            r = f'{userinput} does not match any wikipedia pages. Try another question!'
        except:
            r = 'exception occurs, please ask another question'
        return r

    nlp = en_core_web_lg.load()
    doc1 = nlp(preprocess(intputSen))
    inputsenti = prep.findsenti(intputSen)
    similarity = 0
    bestlist = []

    for x in range(len(doc2)):
        if doc2[x][0].vector_norm and doc1.vector_norm:
            similarity = doc1.similarity(doc2[x][0])  # compare the input sentence and questions stored in the list

        if similarity > 0.60:
            # this is the threshold, so if this value is too high, then your input must
            # have a higher degree of similarity to the questions in the corpora
            index = x
            bestlist.append([similarity, index, doc2[x][1]])
    # if we can not find answers from given copra, then using wolfram
    if len(bestlist) == 0:
        try:
            # api usage see https://products.wolframalpha.com/api/documentation/
            params = {'input': intputSen, 'appid': WOLFRAM_APP_ID, 'output': 'json'}
            r = requests.get(url='http://api.wolframalpha.com/v2/query', params=params)
            j = json.loads(r.content)
            return j['queryresult']['pods'][1]["subpods"][0]["plaintext"]
        except:
            # at least 5 different  reasonable responses when the user enters something outside the two topics
            listReply = ['Sorry your question is not included in my database', 'Sorry, I do not know how to reply that',
                         'Whoops! my brain is dead, may be next question', 'Pass that bro, I cannot remember',
                         'This question is too difficult, next question please',
                         'Your question is hard for me, sorry about that']
            replyOutsideTopic = random.choice(listReply)
            print(replyOutsideTopic)
            return replyOutsideTopic
    sortedanswer = sorted(bestlist, key=operator.itemgetter(0))

    if len(sortedanswer) == 1:
        print(answer[sortedanswer[0][1]])
        return answer[sortedanswer[0][1]]
    else:
        if sortedanswer[-1][0] != sortedanswer[-2][0]:
            print(answer[sortedanswer[-1][1]])
            return answer[sortedanswer[-1][1]]
        else:
            if abs(sortedanswer[-1][2] - inputsenti) > abs(sortedanswer[-2][
                                                               2] - inputsenti):  # if top 2 answer have same similarity, then check the sentiment.
                print(answer[sortedanswer[-2][1]])
                return answer[sortedanswer[-2][1]]
            else:
                print(answer[sortedanswer[-1][1]])
                return answer[sortedanswer[-1][1]]
