import os

import openai
from flask import Flask, redirect, render_template, request, url_for

import fitz

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

m = []

@app.route("/", methods=("GET", "POST"))
def index():
    #if m == []:
        #m.append(add_message("Here is unstructured deck data: \n\n"))
        #m.append(add_message(read_deck()))


    if request.method == "POST":
        if "prompt" in request.form:
            if m == []:
                print("no messages")
                return redirect(url_for("index", result=[add_message("Error: No Deck")]))
            p = request.form["prompt"]
            print("pee")
            print(p)
            m.append(add_message(p))
            r = openapi_request(m)
            m.append(r.choices[0].message)
            return redirect(url_for("index", result=m))
        elif "deck" in request.files:
            f = request.files
            print(f)
            d = request.files["deck"]
            print("reading:")
            print(d)
            if d == "":
                print("Error: empty file")
                return redirect(url_for("index", result=[add_message("Error: Empty file")]))
                
            u = upload_deck(d)
            m.append(add_message(u))
            return redirect(url_for("index", result=m))

    result = request.args.get("result")
    return render_template("index.html", result=m)

def add_message(m):
    return {"role": "user", "content": m}

def to_html(ms):
    for msg in ms:
        msg["content"] = msg["content"].replace('\n', '<br>')
    return

def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )

@app.route("/models", methods=(["GET"]))
def console():
    l = openai.Model.list()
    return(l)

def openapi_request(msg):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msg,
        temperature=0.6,
    )
    #print(response)

    return response

def upload_deck(d):
    print("uplaoding")
    with fitz.open("pdf", d.read()) as doc:  # open document
        text = chr(12).join([page.get_text() for page in doc])
        #print ("number of pages: %i" % doc.page_count)
        print (doc.metadata)

    print("read deck:")
    print(text)
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
            #print ("number of pages: %i" % doc.page_count)
            print (doc.metadata)

        print("read deck:")
        print(text)
        return(text)
        # write as a binary file to support non-ASCII characters
        #pathlib.Path(d[:-4] + ".txt").write_bytes(text.encode())

