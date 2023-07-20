import os

import openai
from flask import Flask, redirect, render_template, request, url_for

import fitz

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

m = []

@app.route("/", methods=("GET", "POST"))
def index():
    if m == []:
        m.append(add_message("Here is unstructured deck data: \n\n"))
        m.append(add_message(read_deck()))


    if request.method == "POST":
        p = request.form["prompt"]
        m.append(add_message(p))
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=m,
            temperature=0.6,
        )
        print(response)
        m.append(response.choices[0].message)
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

