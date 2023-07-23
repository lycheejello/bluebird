import os

import openai
from flask import Flask, Blueprint, g, render_template, request, session

import fitz

openai.api_key = os.getenv('OPENAI_API_KEY')

page = Blueprint('page', __name__, template_folder='templates')
d = None

class Dialogue:
    m = []
    def __init__(self):
        PROMPT = 'Here is unstructured deck data: \n'
        self.add_message(PROMPT)

    def add_message(self,msg):
        self.m.append({'role': 'user', 'content': msg})
        return self.m[-1]

    def add_response(self,msg):
        self.m.append(msg)
        return self.m[-1]

    def err_message(self,msg):
        return [{'role': 'Error', 'content': msg}]

    def reset(self):
        self.m = []
        self.__init__()

def get_dialogue():
    global d
    if d is None:
        print('init d')
        d = Dialogue()
    return d

def create_app():
    app = Flask(__name__)
    app.register_blueprint(page)
    return app
        

@page.route('/', methods=('GET', 'POST'))
def index():

    convo = get_dialogue()

    if request.method == 'POST':
        if 'prompt' in request.form:
            p = request.form['prompt']
            print('prompt')
            print(p)
            convo.add_message(p)
            r = openapi_request(convo.m)
            print(r)
            convo.add_response(r.choices[0].message)
            #return redirect(url_for('index', result=convo.m))
            return render_template('index.html', result=convo.m)
        elif 'deck' in request.files:
            d = request.files['deck']
            print(d)
            if d.filename == '':
                print('Error: empty file')
                print(convo.err_message('Empty File'))
                return render_template('index.html', result=convo.err_message('Empty File'))
                #return redirect(url_for('index', result=convo.err_message('Empty File')))
            else:
                convo.reset()
                u = upload_deck(d)
                convo.add_message(u)
                return render_template('index.html', result=convo.m)
                #return redirect(url_for('index', result=m))

    result = request.args.get('result')
    return render_template('index.html', result=convo.m)

@page.route('/models', methods=(['GET']))
def models():
    l = openai.Model.list()
    return(l)


def openapi_request(msg):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=msg,
        temperature=0.6,
    )
    #print(response)

    return response

def upload_deck(d):
    print('uplaoding')
    with fitz.open('pdf', d.read()) as doc:  # open document
        text = chr(12).join([page.get_text() for page in doc])
        #print ('number of pages: %i' % doc.page_count)
        print (doc.metadata)

    return(text)

def read_deck():

    DECKS = (r'./Decks')
    files = os.listdir(DECKS)

    for d in files:
        doc_path = os.path.join(DECKS, d)
        #text = None

        #print(doc_path)

        with fitz.open(doc_path) as doc:  # open document
            text = chr(12).join([page.get_text() for page in doc])
            #print ('number of pages: %i' % doc.page_count)
            print (doc.metadata)

        print('read deck:')
        print(text)
        return(text)
        # write as a binary file to support non-ASCII characters
        #pathlib.Path(d[:-4] + '.txt').write_bytes(text.encode())

