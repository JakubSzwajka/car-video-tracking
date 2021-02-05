from urllib.request import urlopen
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "odpowiedź z serwera"

if __name__ == "__main__": 
    app.run()
