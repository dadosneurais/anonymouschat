from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv
import os


app = Flask(__name__)
load_dotenv()

# take the msg to memory in list
mensagens = []


### mongo ###
client = MongoClient(os.getenv("MONGO_URI"))
db = client["db_anonymous"]
logs_collection = db["text"]

def save(msg):

    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    logs_collection.insert_one({
        "texto": msg,
        "data": (datetime.now(timezone.utc) - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
        "ip": ip
    })
#############

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        texto = request.form.get('texto')
        if texto:
            brtime = (datetime.now(timezone.utc) - timedelta(hours=3)).strftime('%H:%M')

            mensagens.append(f'{texto} - {brtime}')
            save(texto) # mongo function to save texto
        return redirect(url_for('index'))
        
    return render_template('index.html', mensagens=mensagens)


@app.route('/msgs')
def msgs():
    return jsonify(mensagens)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
