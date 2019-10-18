import flask
import pickle
from flask import Flask, render_template,request
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import make_pipeline
from nltk.corpus import stopwords
import re
import json
import contractions


wnl = WordNetLemmatizer()
remove =set(stopwords.words('english'))
def edit(words):
    words =str(words)
    words=re.sub('([.,////])',' ',words)
    words=re.sub('\[.*?\]', '', words)
    words = words.replace('\n', ' ')
    words = contractions.fix(words)
    word_list = nltk.word_tokenize(re.sub(r'([^a-z A-Z])', '', words.lower()))
    comment = ' '.join([wnl.lemmatize(w) for w in word_list if w not in remove])
    return comment
user ={}
app = Flask(__name__)

@app.route('/')
def index():
	return "Flask server"

@app.route('/query', methods = ['POST'])
def postdata():
    data = request.get_json()
    loaded_model = pickle.load(open("model(2).pkl","rb"))
    q = data['query']
    u = data['user']
    q =q.split(';')[0]
    q = q.split('+')
    q=' '.join(q)
    q = edit(q)
    print(q)
    result=loaded_model.predict([q])
    result=result[0]
    if result ==1:
        x = 'true'
    else:
        x = 'false'
    print(x)
    if result ==1:
        user[u]=x
    elif u in user.keys():
        pass
    else:
        user[u]=x
    # do something with this data variable that contains the data from the node server
    return json.dumps({"mentalstate":x})

@app.route('/user', methods = ['POST'])
def new():
    data1 = request.get_json()
    email = data1['email']
    if email in user.keys():
        return json.dumps({"mentalstate":user[email]})
    else:
        return json.dumps({"mentalstate":"NULL"})

if __name__ == "__main__":
	app.run(debug = True,host='0.0.0.0')
