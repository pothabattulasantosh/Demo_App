import os
os.environ['KERAS_BACKEND'] = 'theano' #theano
import config
import keras #keras
from keras.models import load_model
from keras.preprocessing import sequence
from keras.preprocessing.sequence import pad_sequences
from flask import jsonify
import numpy as np #numpy
import joblib #joblib
import re
from bs4 import BeautifulSoup #beautifulsoup4 ,lxml




model = load_model(config.MODEL_PATH)
tokens = joblib.load(config.TOKENS_PATH)
AUX_LABELS = np.asarray(config.AUX_LABELS)
IDENTIY_LABELS = np.asarray(config.IDENTIY_LABELS)



def  validateParams(name,comment):
    if (len(name))<config.NAME_MIN_LEN:
        retJson = {'status':301,'Error': 'Please type valid Name'}
        return retJson
    if (len(comment))<config.CMT_MIN_LEN:
         retJson = {'status':301,'Error': f'Please make sure your comment has atleast {config.CMT_MIN_LEN} characters'}
         return retJson
    retJson = {
        'status':200
        }

    return retJson

def preProcess(comment):#To Do
        # https://stackoverflow.com/a/47091490/4084039
    def decontracted(phrase):
        # specific
        phrase = re.sub(r"won't", "will not", phrase)
        phrase = re.sub(r"can\'t", "can not", phrase)

        # general
        phrase = re.sub(r"n\'t", " not", phrase)
        phrase = re.sub(r"\'re", " are", phrase)
        phrase = re.sub(r"\'s", " is", phrase)
        phrase = re.sub(r"\'d", " would", phrase)
        phrase = re.sub(r"\'ll", " will", phrase)
        phrase = re.sub(r"\'t", " not", phrase)
        phrase = re.sub(r"\'ve", " have", phrase)
        phrase = re.sub(r"\'m", " am", phrase)
        return phrase

    sentance = re.sub(r"http\S+", "", comment)
    sentance = BeautifulSoup(sentance, 'lxml').get_text()
    sentance = decontracted(sentance)
    sentance = re.sub("\S*\d\S*", "", sentance).strip()
    sentance = re.sub('[^A-Za-z]+', ' ', sentance)
    # https://gist.github.com/sebleier/554280
    sentance = ' '.join(e.lower() for e in sentance.split() if e.lower() not in config.STOP_WORDS)
    return sentance.strip()

def evaluteToxicity(comment):#To do
    if len(comment)<=3:
        return "Please make sure to enter meaningful secentance elaboratively, so that I can able to judge"
    sequence=tokens.texts_to_sequences([comment])
    sequence= pad_sequences(sequence, maxlen=500, padding='post')
    predictions = model.predict(sequence)
    target = predictions[0]
    aux_label = AUX_LABELS[np.argsort(-predictions[1])][0][:3]
    identity_label=IDENTIY_LABELS[np.argsort(-predictions[2])][0][:3]

    if target<0.5:
        msg = config.pos_msg
    else:
        msg =  config.neg_msg[0]+' '+str(identity_label[0])+' or '+str(identity_label[1])+' or '+str(identity_label[2])+'. '+config.neg_msg[1]+' '+str(aux_label[0])+', '+str(aux_label[1])+' and '+str(aux_label[2])

    return msg
